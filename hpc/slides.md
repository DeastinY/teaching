---
title: Cluster Introduction
theme: moon #solarized
separator: ---
verticalSeparator: <!--v-->
revealOptions:
  transition: 'slide'
  auto-animate: true
---

## Getting started with High Performance Computing in Research
_Richard Polzin <rpolzin@ukaachen.de\>_  
###### Last Updated: 27. Nov 2024  

---

### Table of Content

1. Introduction <!-- .element: class="fragment" data-fragment-index="1" -->
2. HPC.NRW Linux Basics for HPC <!-- .element: class="fragment" data-fragment-index="2" -->
3. Tips and Tricks <!-- .element: class="fragment" data-fragment-index="3" -->
4. SLURM Job Manager <!-- .element: class="fragment" data-fragment-index="4" -->
5. Compute Time Application <!-- .element: class="fragment" data-fragment-index="4" -->


---

# Introduction

<!--v-->

### Objectives
- Understand what HPC is
- Learn why HPC is essential for modern research
- Discover available HPC resources
- Walk through a project application process

<!--v-->
<!-- .slide: data-auto-animate -->
## What is HPC?<!-- .element: data-id="code-animation"-->

- **H**igh **P**erformance **C**omputing involves the use of supercomputers and parallel processing techniques to solve complex computational problems
- Combines computing resources for higher performance
- HPC Systems consist of clusters with interconnected nodes
- Enable processing larger datasets and complex simulations

<!--v-->
<!-- .slide: data-auto-animate -->
## What is HPC?<!-- .element: data-id="code-animation"-->

![](claix23.png)

<!--v-->

## Why is HPC Essential?

- **Speed:** Reduces time to results
- **Capacity:** Handle large scale data and simulation
- **Complexity:** Solve problems to complex for standard computers

<!--v-->
<!-- .slide: data-auto-animate -->
## HPC Resources<!-- .element: data-id="code-animation"-->

- **State of the art** HPC facilities are available through the National High Performance Computing (NHR) network
- Including Compute Clusters, Large Scale Storage, and advanced networking infrastructure

<!--v-->

## Access Eligibility and Requirements

- Researchers, students, and collaborators from German Universities
- University credentials (TIM-ID) are required
- Compliance with university and HPC usage policy is expected
- Resources are to be used responsible

<!--v-->
<!-- .slide: data-auto-animate -->
## HPC Resources<!-- .element: data-id="code-animation"-->

![](nhr.png)

<!--v-->
<!-- .slide: data-auto-animate -->
## The RWTH Compute Cluster <!-- .element: data-id="code-animation"-->

Per Node:
  - 2x Intel Xeon 8468 (48 core CPU)
  - 1.5 TB local SSD Storage
  - 256GB - 1,024GB of RAM
  - 632 such notes available

<!--v-->
<!-- .slide: data-auto-animate -->
## The RWTH Compute Cluster <!-- .element: data-id="code-animation"-->

Per Node (ML):
  - 2x Intel Xeon 8468
  - 695 GB local SSD Storage
  - 512GB of RAM
  - 4 x NVIDIA H100 GPU (96GB HBM2e)
  - 52 such notes available

<!--v-->

### Account Creation

Use Selfservice to create your account   
(https://idm.rwth-aachen.de/selfservice/)
1. Accounts and Passwords
2. Account Overview
3. Create HPC Account

<!--v-->

<!-- .slide: data-auto-animate -->
### Login

```zsh
ssh ab1234@login23-1.hpc-itc.rwth-aachen.de
```

- Login with secure shell (ssh): **ssh tim@host**
- Needs VPN if not connected to eduroam
- d*Different nodes available for different use cases*

<!--v-->

### Cluster Access Nodes

Use the appropriate node for your task.  
Be considerate of shared resources.

- Login Nodes
  - lightweight tasks (script editing, testing)
- Copy Nodes
  - Optimized for data transfer

<!--v-->

![overview of different login nodes](login-nodes.png) <!-- .element height="80%" width="80%" -->

<!--v-->

### The File Systems

- **$HOME:** Small quote, backed up. For scripts and small files.
- **$WORK:** Large quote, not backed up. For working with many small files.
- **$HPCWORK:** Largest quote, not backed up. For I/O intense jobs and large files.

<!--v-->

![](filesystems.png)

<!--v-->

### Data Transfer Methods

- Use copy nodes for data transfer
- Consider data security and encryption
- Terminal: *scp* or *rsync*
- Mount as folder: *sshfs*

<!--v-->
### Project Management

- Groups are created for every project
- Every group consists of owners (PC/PI), Managers and Members
- Granted computation time and storage space is shared through groups
- In Aachen project storage is deleted **8 months** after a project's conclusion. Make sure you migrate the data by then!

<!--v-->
### Project Management

Users can be added to and removed from groups/projects using their TIM-ID.
```sh
member add --name <project-id> <user-id>
member delete --name <project-id> <user-id>
member finger # view group affiliations
```
- append **--manager** to any command above to assign or revoke the manager role

<!--v-->
### Summary of this Chapter
- HPC enables advanced computational research
- NHR provides access to free HPC resources
- Account creation and cluster access
- File System and Project management

---
> The following slides are adapted from the HPC.NRW Competency Network under the CC-BY-SA license. Check out their work at https://hpc-wiki.info/hpc/HPC_Wiki
---
## Background and History
<!--v-->
![](hpc.nrw/01_0002.png)
<!--v-->
![](hpc.nrw/01_0003.png)
<!--v-->
![](hpc.nrw/01_0004.png)
<!--v-->
![](hpc.nrw/01_0005.png)
---
## The Command Line
<!--v-->
![](hpc.nrw/02_0002.png)
<!--v-->
![](hpc.nrw/02_0003.png)
<!--v-->
![](hpc.nrw/02_0004.png)
<!--v-->
![](hpc.nrw/02_0005.png)
<!--v-->
![](hpc.nrw/02_0006.png)
<!--v-->
![](hpc.nrw/02_0007.png)
<!--v-->
![](hpc.nrw/02_0008.png)
<!--v-->
![](hpc.nrw/02_0009.png)
---
## Directory Structure
<!--v-->
![](hpc.nrw/03_0002.png)
<!--v-->
![](hpc.nrw/03_0003.png)
<!--v-->
![](hpc.nrw/03_0004.png)
<!--v-->
![](hpc.nrw/03_0005.png)
<!--v-->
![](hpc.nrw/03_0006.png)
<!--v-->
![](hpc.nrw/03_0007.png)
<!--v-->
![](hpc.nrw/03_0008.png)
---
## Files
<!--v-->
![](hpc.nrw/04_0002.png)
<!--v-->
![](hpc.nrw/04_0003.png)
<!--v-->
![](hpc.nrw/04_0004.png)
<!--v-->
![](hpc.nrw/04_0005.png)
<!--v-->
![](hpc.nrw/04_0006.png)
<!--v-->
![](hpc.nrw/04_0007.png)
---
## Text Display and Search
<!--v-->
![](hpc.nrw/05_0002.png)
<!--v-->
![](hpc.nrw/05_0003.png)
<!--v-->
![](hpc.nrw/05_0004.png)
<!--v-->
![](hpc.nrw/05_0005.png)
<!--v-->
![](hpc.nrw/05_0006.png)
<!--v-->
![](hpc.nrw/05_0007.png)
---
## Users and Permissions
<!--v-->
![](hpc.nrw/06_0002.png)
<!--v-->
![](hpc.nrw/06_0003.png)
<!--v-->
![](hpc.nrw/06_0004.png)
<!--v-->
![](hpc.nrw/06_0005.png)
<!--v-->
![](hpc.nrw/06_0006.png)
<!--v-->
![](hpc.nrw/06_0007.png)
---
## Processes
<!--v-->
![](hpc.nrw/07_0002.png)
<!--v-->
![](hpc.nrw/07_0003.png)
<!--v-->
![](hpc.nrw/07_0004.png)
<!--v-->
![](hpc.nrw/07_0005.png)
---
## The vim Text editor
<!--v-->
![](hpc.nrw/08_0002.png)
<!--v-->
![](hpc.nrw/08_0003.png)
<!--v-->
![](hpc.nrw/08_0004.png)
<!--v-->
![](hpc.nrw/08_0005.png)
<!--v-->
![](hpc.nrw/08_0006.png)
<!--v-->
![](hpc.nrw/08_0007.png)
<!--v-->
![](hpc.nrw/08_0008.png)
<!--v-->
![](hpc.nrw/08_0009.png)
---
## Shell Scripts
<!--v-->
![](hpc.nrw/09_0002.png)
<!--v-->
![](hpc.nrw/09_0003.png)
<!--v-->
![](hpc.nrw/09_0004.png)
<!--v-->
![](hpc.nrw/09_0005.png)
<!--v-->
![](hpc.nrw/09_0006.png)
<!--v-->
![](hpc.nrw/09_0007.png)
<!--v-->
![](hpc.nrw/09_0008.png)
---
## Environment Variables
<!--v-->
![](hpc.nrw/10_0002.png)
<!--v-->
![](hpc.nrw/10_0003.png)
<!--v-->
![](hpc.nrw/10_0004.png)
<!--v-->
![](hpc.nrw/10_0005.png)
<!--v-->
![](hpc.nrw/10_0006.png)
---
## System Configuration
<!--v-->
![](hpc.nrw/11_0002.png)
<!--v-->
![](hpc.nrw/11_0003.png)
<!--v-->
![](hpc.nrw/11_0004.png)
<!--v-->
![](hpc.nrw/11_0005.png)
<!--v-->
![](hpc.nrw/11_0006.png)
<!--v-->
![](hpc.nrw/11_0007.png)
---
## SSH Connections
<!--v-->
![](hpc.nrw/12_0002.png)
<!--v-->
![](hpc.nrw/12_0003.png)
<!--v-->
![](hpc.nrw/12_0004.png)
<!--v-->
![](hpc.nrw/12_0005.png)
<!--v-->
![](hpc.nrw/12_0006.png)
<!--v-->
![](hpc.nrw/12_0007.png)
<!--v-->
![](hpc.nrw/12_0008.png)
<!--v-->
![](hpc.nrw/12_0009.png)
---

<!-- .slide: data-auto-animate -->
## Tips and Tricks <!-- .element: data-id="code-animation"-->

This is a collection of tips and tricks that make working with the cluster easier and more convenient.

<!--v-->

<!-- .slide: data-auto-animate -->
## Tips and Tricks <!-- .element: data-id="code-animation"-->

1. You can mount the remote cluster file system to your local machine

```zsh
sshfs ab1234@copy23node:/home/ab1234 /mnt/clusterhome
```
<!-- .element: class="fragment" data-fragment-index="1" -->
<!--v-->

<!-- .slide: data-auto-animate -->
## Tips and Tricks <!-- .element: data-id="code-animation"-->

1. You can mount the remote cluster file system to your local machine

```zsh
sshfs ab1234@copy23node:/home/ab1234 /mnt/clusterhome
```

unmount with: 
```zsh
sudo umount -l /mnt/clusterhome
```

<!--v-->

<!-- .slide: data-auto-animate -->

## Tips and Tricks <!-- .element: data-id="code-animation"-->

2. If you are outside of eduroam, you can connect through VPN and access the cluster *everywhere*
    
Go to http://help.itc.rwth-aachen.de  
and search for "VPN"

---

<!-- .slide: data-auto-animate -->

## SLURM Job Manager <!-- .element: data-id="code-animation"-->

**S**imple **L**inux **U**tility for **R**esource **M**anagement

- Job scheduler often used in supercomputers and compute clusters <!-- .element: class="fragment" data-fragment-index="1" -->
- Provides many advantages for utilizing HPC hardware with many users, such as..  <!-- .element: class="fragment" data-fragment-index="2" -->
  - ... Accounting, Containerization, Priorities, Chain- and Array-Jobs, ... <!-- .element: class="fragment" data-fragment-index="2" -->

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

- Users can interact with SLURM from login nodes <!-- .element: class="fragment" data-fragment-index="1" -->
- Users may request cores, memory and time, then send their programs to be queued  <!-- .element: class="fragment" data-fragment-index="2" -->
- SLURM reserves these resources and waits till they are available <!-- .element: class="fragment" data-fragment-index="3" -->
- Once available, the code will then be run <!-- .element: class="fragment" data-fragment-index="4" -->

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

![](slurm.png)

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

SLURM is fed **jobscripts**, which contain all information the scheduler needs to run a program

These jobscripts consist of three parts:

1. Shebang <!-- .element: class="fragment" data-fragment-index="1" -->
2. Job Parameters <!-- .element: class="fragment" data-fragment-index="2" --> 
3. Actual Job Code <!-- .element: class="fragment" data-fragment-index="3" -->

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Example

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Example

```sh
#!/usr/bin/zsh
```
<!-- .element: data-id="code-animation"-->

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Example

```sh
#!/usr/bin/zsh

### Job Parameters
#SBATCH --cpus-per-task=8              
#SBATCH --time=00:15:00         
#SBATCH --job-name=example_job  
#SBATCH --output=stdout.txt     
#SBATCH --account=<project-id>
```
<!-- .element: data-id="code-animation"-->

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Example

```sh
#!/usr/bin/zsh

### Job Parameters
#SBATCH --cpus-per-task=8              
#SBATCH --time=00:15:00         
#SBATCH --job-name=example_job  
#SBATCH --output=stdout.txt     
#SBATCH --account=<project-id>

### Program Code
echo "Hello SLURM"
```
<!-- .element: data-id="code-animation"-->

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Example

- Safe the file
- Submit the job <!-- .element: class="fragment" data-fragment-index="1" -->
```sh
> sbatch testjob.sh
```
<!-- .element: class="fragment" data-fragment-index="2" -->
- Check its state <!-- .element: class="fragment" data-fragment-index="3" -->
```sh
> squeue --me
JOBID     PARTITION  NAME        USER      ST    TIME  NODES 
12345678  c23ms      example_job AB123456  R     0:02      1
```
<!-- .element: class="fragment" data-fragment-index="4" -->

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Common Parameters

- Number of cores: **-c /--cpus-per-task \<numpcus>**
- Memory: **-m /--mem=\<amount>G**
- Human readable Job name: **-J /--job-name**
- Reporting File: **-o /--output=\<filename>**
- Runtime: **-t /--time=d-hh:mm:ss**
- Account: **-A /--account=\<project>**
- GPUs: **--gres=gpu:\<type>:\<amount>**


<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Commands in a Nutshell

Submit jobs
```sh
> sbatch <BATCH_SCRIPT> [ADDITIONAL ARGUMENTS]
```

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Commands in a Nutshell

Display Job Queue
```sh
> squeue [OPTIONS]
```
**--me** shows only your jobs  
**--start** shows the estimated starttime  
**--format** can be used to filter e.g. for GPU jobs

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Commands in a Nutshell

Cancel Jobs
```sh
> scancel [OPTIONS] <JOB-ID>
```
**--me** cancel all of your jobs  
**--v** provide details of the cancellation process  

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Commands in a Nutshell

Request an interactive job
```sh
> salloc [OPTIONS]
```
Job parameters just like in the jobscript. Redirects the shell to the head node. Job ends when the shell terminates.
```sh
salloc --gres=gpu:1 -n 24 -t 1:00:00 # 24c+GPU node for 1 hour
```
<!-- .element: class="fragment" data-fragment-index="1" -->

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Commands in a Nutshell

Display Accounting Information
```sh
> sacct [OPTIONS]
```
Print details abound pending, running, or past jobs.
```sh
> sacct -S $(date -I --date="yesterday")
```
Would show all jobs submitted since yesterday.

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

#### Commands in a Nutshell
```sh
> r_wlm_usage
```
Command for only the RWTH HPC to display available / used resources against the account / group quota

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

Monitoring tools are improving constantly, with *perfmon* currently being established across compute clusters

<!--v-->

<!-- .slide: data-auto-animate -->
## SLURM Job Manager <!-- .element: data-id="code-animation"-->

![](grafana.png)

---

<!-- .slide: data-auto-animate -->
## Compute Time Application <!-- .element: data-id="code-animation"-->
- Resources are measured in core hours (core-h) <!-- .element: class="fragment" data-fragment-index="1" -->
    - A Macbook Pro has roughly 70k core-h/year <!-- .element: class="fragment" data-fragment-index="2" -->
- The smallest project already guarantees 360k core-h <!-- .element: class="fragment" data-fragment-index="3" -->
- Estimate your needs based on previous work <!-- .element: class="fragment" data-fragment-index="4" -->
- Write and submit your application! <!-- .element: class="fragment" data-fragment-index="5" -->

<!--v-->

<!-- .slide: data-auto-animate -->
## Compute Time Application <!-- .element: data-id="code-animation"-->

HPC resources in Germany are arranged hierarchically in the HPC Performance Pyramid.
- **Tier-0**: PRACE and EuroHPC
- **Tier-1**: Gauss Center for Supercomputing (GCS, JSC, HLRS, LRZ)
- **Tier-2**: HPC Centres with supra-regional tasks and thematically dedicated HPC/centres
- **Tier-3**: Regional HPC centres

<!--v-->

<!-- .slide: data-auto-animate -->
## Compute Time Application <!-- .element: data-id="code-animation"-->

![alt text](image-2.png)

<!--v-->

<!-- .slide: data-auto-animate -->
## Compute Time Application <!-- .element: data-id="code-animation"-->

![](computetime.jpg)

<!--v-->

![](nhr.png)

<!--v-->

![](nhrprocess.jpg)

<!--v-->

### Acknowledgement (RWTH/JARA)

*Computations were performed with computing resources granted by RWTH Aachen University under project <ID of your project>.*

<!--v-->

### Acknowledgement (RWTH/JARA)

*The authors gratefully acknowledge the computing time provided to them at the NHR Center NHR4CES at RWTH Aachen University (project number <your-project-id: p0020XXX>). This is funded by the Federal Ministry of Education and Research, and the state governments participating on the basis of the resolutions of the GWK for national high performance computing at universities (www.nhr-verein.de/unsere-partner).*

---

### Any Questions?
