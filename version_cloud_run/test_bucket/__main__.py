"""A Google Cloud Python Pulumi program"""

import pulumi
import pulumi_gcp as gcp

# Create a GCP resource (Storage Bucket)
bucket = gcp.storage.Bucket("my-bucket",
    location="northamerica-northeast1",
    uniform_bucket_level_access=True,
    website={
        "mainPageSuffix": "index.html"
    }
)

bucket_iam_binding = gcp.storage.BucketIAMBinding("my-bucket-IAMBinding",
    bucket=bucket.name,
    role="roles/storage.objectViewer",
    members=["allUsers"]
)

bucket_object = gcp.storage.BucketObject("index.html",
    bucket=bucket.name,
    content_type="text/html",
    source=pulumi.asset.FileAsset("index.html")
)

# Export the DNS name of the bucket
bucket_name = bucket.url
bucket_endpoint = pulumi.Output.concat("http://storage.googleapis.com/", bucket.name, "/", bucket_object.name)

# Export the outputs
pulumi.export("bucketName", bucket_name)
pulumi.export("bucketEndpoint", bucket_endpoint)
