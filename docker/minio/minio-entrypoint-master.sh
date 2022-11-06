#!/bin/sh

mc alias set source http://minio-server-master:9000 minio-root-user-master minio-root-password-master
mc alias set dest http://minio-server-node1:9000 minio-root-user-node1 minio-root-password-node1

# Create buckets with versioning and object locking enabled.
mc mb -l source/bucket
mc mb -l dest/bucket

### Create a replication admin on source alias
# create a replication admin user : repladmin
mc admin user add source repladmin repladmin123

# create a replication policy for repladmin
cat > repladmin-policy-source.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "admin:SetBucketTarget",
                "admin:GetBucketTarget"
            ],
            "Effect": "Allow",
            "Sid": "EnableRemoteBucketConfiguration"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetReplicationConfiguration",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads",
                "s3:GetBucketLocation",
                "s3:GetBucketVersioning",
                "s3:GetObjectRetention",
                "s3:GetObjectLegalHold",
                "s3:PutReplicationConfiguration"
            ],
            "Resource": [
                "arn:aws:s3:::*"
            ],
            "Sid": "EnableReplicationRuleConfiguration"
        }
    ]
}
EOF
mc admin policy add source repladmin-policy ./repladmin-policy-source.json
cat ./repladmin-policy-source.json

#assign this replication policy to repladmin
mc admin policy set source repladmin-policy user=repladmin

### on dest alias
# Create a replication user : repluser on dest alias
mc admin user add dest repluser repluser123

# create a replication policy for repluser
# Remove "s3:GetBucketObjectLockConfiguration" if object locking is not enabled, i.e. bucket was not created with `mc mb --with-lock` option
# Remove "s3:ReplicateDelete" if delete marker replication is not required
cat > replpolicy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetReplicationConfiguration",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads",
                "s3:GetBucketLocation",
                "s3:GetBucketVersioning",
                "s3:GetBucketObjectLockConfiguration",
                "s3:GetEncryptionConfiguration"
            ],
            "Resource": [
                "arn:aws:s3:::*"
            ],
            "Sid": "EnableReplicationOnBucket"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetReplicationConfiguration",
                "s3:ReplicateTags",
                "s3:AbortMultipartUpload",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:GetObjectVersionTagging",
                "s3:PutObject",
                "s3:PutObjectRetention",
                "s3:PutBucketObjectLockConfiguration",
                "s3:PutObjectLegalHold",
                "s3:DeleteObject",
                "s3:ReplicateObject",
                "s3:ReplicateDelete"
            ],
            "Resource": [
                "arn:aws:s3:::*"
            ],
            "Sid": "EnableReplicatingDataIntoBucket"
        }
    ]
}
EOF
mc admin policy add dest replpolicy ./replpolicy.json
cat ./replpolicy.json

# assign this replication policy to repluser
mc admin policy set dest replpolicy user=repluser

# define remote target for replication from source/bucket -> dest/bucket
mc admin bucket remote add source/bucket http://repluser:repluser123@minio-server-node1:9000/bucket --service "replication" --json > remote_arn.json

remote_string=$(grep -Po '"RemoteARN":.*?[^\\]",' remote_arn.json)

arn_address="${remote_string:13:-2}"

echo "Now, use this ARN to add replication rules using 'mc replicate add' command:"
echo "${arn_address}"

# use arn returned by above command to create a replication policy on the source/bucket with `mc replicate add`
mc replicate add source/bucket --priority 1 --remote-bucket "${arn_address}" \
   --replicate existing-objects,delete,delete-marker,replica-metadata-sync