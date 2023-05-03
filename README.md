# DHIS2 Demo

This capture the steps required to run a local copy of DHIS2.

## TODO

- [ ] Find an engagement owner - permission to stand up a VM?
- [x] Deploy local
- [x] Deploy to VM - docker-compose
  - [x] pulumi - gcp - vm - docker-compose
  - [x] install docker with init script
  - [ ] move to pulumi/{quickstart|docker-vm} directory
  - [ ] move to phac-garden
  - [ ] with caddy for ssl
  - [ ] tune instance type
    - e2-medium     // 1-2 vCPU (1 shared core), 4 GB memory
    - e2-standard-2 // 2 vCPU, 8 GB memory
    - e2-standard-4 // 4 vCPU, 16 GB memory

## Pulumi

Select the backend and setup gcloud auth

```bash
# Select the state backend (local)

# From repo top level - until we start using a GCP bucket for state
mkdir PulumiState && pulumi login "file:$PWD/PulumiState"
pulumi login file:/Users/daniel/Code/PHAC/phac-dhis2/PulumiState
# required to operate on GCP
gcloud auth application-default login
```

### GCP-VM-Docker - GCP

```bash
mkdir docker-vm && cd docker-vm
pulumi new gcp-typescript
# set the project scope
pulumi config set gcp:project pdcp-cloud-009-danl
pulumi up
```

#### ssh into the vm

```bash
# All the outputs
pulumi stack output
# get the external ip
pulumi stack output externalIP

# add user to docker group: 'till I figure out how to get the $USER in the init script
gcloud compute ssh --zone "$(pulumi stack output instanceZone)" "$(pulumi stack output instanceName)" --command 'sudo usermod -aG docker $USER'

# ssh into the machine
gcloud compute ssh --zone "$(pulumi stack output instanceZone)" "$(pulumi stack output instanceName)" 


```

#### Cleanup

```bash
# clean up resources
pulumi destroy
# remove 'dev' stack and history
pulumi stack rm dev
```

### QuickStart - WebBucket

Start a GCP typescript pulumi project with local state

```bash
mkdir quickstart && cd quickstart
pulumi new gcp-typescript
# set the project scope
pulumi config set gcp:project pdcp-cloud-009-danl
pulumi up
# clean up resources
pulumi destroy
# remove 'dev' stack and history
pulumi stack rm dev
```

## Log (external)

- 2023-04-19 - DHIS2 demo - with Diana
- 2023-04-11 - Setting up DHIS2 w/Diana,Jenny, Elizaveta, Sujani
  - They will look at [demo site](https://dhis2.org/demo/)
  - Start GCP account creation? w/John
- 2023-04-04 - Sujani on Teams: Meeting at 09h00 (Elizaveta is away)
  - Follow up - Who can own this project?
- 2023-03-30 1-1 w/Elizaveta Oulman (SRHD)
- 2023-03-23 - docker-compose (spaces) GitHub: DHIS2 (github.com)
- 2023-03-22 - Tim: Can you look at DHIS2
- 2023-03-16 - Susan - CSAR+ODK meeting - Harms Reduction / Elizaveta Oulman - DMIA Intake Team?

## Org

- Sujani, Lisa, Elizaveta are intake team - DST Team - Data Science Team
- Diana, Jenny, Amanda SRHD - Substance Realated Harms Division

## References

- [DHIS2 Core Repo](https://github.com/dhis2/dhis2-core)
- [DHIS2 Implementation Guide](https://docs.dhis2.org/en/implement/implement.html)
- [DHIS2 Developer Portal](https://developers.dhis2.org/)
- [Developer Portal Repo](https://github.com/dhis2/developer-portal)
- [Code Repo](https://github.com/dhis2/dhis2-core#run-dhis2-in-docker)
- [Pulumi AI](https://www.pulumi.com/ai/)
