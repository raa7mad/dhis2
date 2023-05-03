import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";

// Create a GCP resource (Storage Bucket)
const bucket = new gcp.storage.Bucket("my-bucket", {
  location: "northamerica-northeast1",
  uniformBucketLevelAccess: true, // Enable Uniform Bucket-Level Access
});

// Export the DNS name of the bucket
export const bucketName = bucket.url;
