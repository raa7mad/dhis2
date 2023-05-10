import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";
// import * as docker from "@pulumi/docker";

// Create the VPC.
const network = new gcp.compute.Network("network", {
  //   region: "northamerica-northeast1",
  autoCreateSubnetworks: false,
  routingMode: "REGIONAL",
});

// Create a Subnetwork within the VPC.
const subnetwork = new gcp.compute.Subnetwork("subnetwork", {
  network: network.selfLink,
  ipCidrRange: "10.2.0.0/16",
  region: "northamerica-northeast1",
});

// Allow SSH access.
const firewall = new gcp.compute.Firewall("allow-ssh-http-https", {
  network: network.selfLink,
  allows: [
    {
      protocol: "tcp",
      ports: ["22", "80", "443", "8080"],
    },
  ],
  targetTags: ["allow-ssh-http-https"],
  sourceRanges: ["0.0.0.0/0"],
});

// Create a static IP address.
const staticIP = new gcp.compute.Address("static-ip", {
  region: "northamerica-northeast1",
});

// Find Ubuntu 22.04 LTS image.
// gcloud compute images list --filter="family~'ubuntu-2204-lts'"
const image = gcp.compute.getImage({
  project: "ubuntu-os-cloud",
  family: "ubuntu-2204-lts",
});

// Install Docker and give SSH access via Metadata.
// This docker install is not recommended for production.
const startupScript = `#!/bin/bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
ufw allow 22
`;

// Create the VM Instance.
const instance = new gcp.compute.Instance("vm-instance", {
  zone: "northamerica-northeast1-a",
  machineType: "e2-medium", //  1-2 vCPU (1 shared core), 4 GB memory
  //  e2-standard-2 // 2 vCPU, 8 GB memory
  //  e2-standard-4 // 4 vCPU, 16 GB memory
  bootDisk: {
    initializeParams: {
      image: image.then((image) => image.selfLink),
      size: 100, // 100GB disk
      type: "pd-ssd",
    },
  },
  networkInterfaces: [
    {
      network: network.selfLink,
      subnetwork: subnetwork.selfLink,
      accessConfigs: [
        {
          natIp: staticIP.address,
        },
      ],
    },
  ],
  metadataStartupScript: startupScript,

  // This is a network tag (used in the firewall rule)
  tags: ["allow-ssh-http-https"],
});

// Export instance name and zone.
export const instanceName = instance.name;
export const instanceZone = instance.zone;
// Export instance external IP.
export const externalIP = staticIP.address;
