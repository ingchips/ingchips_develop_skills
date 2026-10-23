# Download FreeRTOS

Download the latest FreeRTOS and Long Term Support (LTS) packages below.

The [FAQ](https://www.freertos.org/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning/#how-are-freertos-git-repositories-structured) describes the difference between individual libraries and library packages, and
provides [links to individual library repositories](https://www.freertos.org/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning/#how-do-i-obtain-and-use-individual-freertos-libraries).

```jsx

```

Find information on [known issues and security updates](#known-issues-with-the-current-release) at the end of this page.


## Security updates

See the [Security Updates](https://www.freertos.org/Security/03-Vulnerabilities) page.


## Next Steps

The development activity for FreeRTOS has migrated from SVN to GitHub and can now be found directly on
our [GitHub organization](https://github.com/FreeRTOS). Download
a [previous release](https://github.com/FreeRTOS/FreeRTOS/releases) of FreeRTOS from GitHub as a standard
zip (.zip) or self-extracting zip file (.exe). Unzip the source code while making sure to maintain the
folder structure. Please read the documentation referenced below to understand the directory structure and get
started quickly!

```jsx









```


## Security Updates

See the [Security Updates](https://www.freertos.org/Security/03-Vulnerabilities) page.

## Upgrade Instructions

* [Upgrading from FreeRTOS V10.4.6 to V10.5.0](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/08-FreeRTOS-V10.5.0)
* [Upgrading from FreeRTOS V10.4.5 to V10.4.6](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/07-FreeRTOS-V10.4.6)
* [Upgrading from FreeRTOS V10.4.4 to V10.4.5](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/06-FreeRTOS-V10.4.5)
* [Upgrading From FreeRTOS V10.3.0 to V10.4.x](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/05-FreeRTOS-V10.4.x)
* [Upgrading From FreeRTOS V10.2.1 to V10.3.0](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/04-FreeRTOS-V10.3.0)
* [Upgrading to FreeRTOS Version 10](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/03-FreeRTOS-V10)
* [Upgrading to FreeRTOS Version 9](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/02-FreeRTOS-V9)
* [Upgrading to FreeRTOS V8.x.x From FreeRTOS V7.x.x](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/01-FreeRTOS-V8)


## Known Issues with the Current Release

### Legacy Issues

#### Coldfire V2 CodeWarrior port

The Coldfire V2 CodeWarrior code will not run with the latest (Eclipse) based CodeWarrior tools. A fix is
posted [on the support forum](https://forums.freertos.org/t/starting-a-simple-task/5743) (post 4), and will
be incorporated into the main release in due course.


#### Coldfire V1 CodeWarrior port

The Coldfire V1 CodeWarrior projects will not automatically update to later CodeWarrior versions unless all
unnecessary files are deleted from the FreeRTOS/Source directory first.
See [this support thread](https://forums.freertos.org/t/project-from-scrap-problems-mcf51cn/653) for more information.


#### MSP430 CrossWorks and GCC demos

The CrossWorks demo has not yet been updated to use CrossWorks V2.0 or later. The GCC demo has not yet been
updated to use the latest MSPGCC compiler version.


#### AVR32 demos

The IAR Embedded Workbench demos for the AVR32 will not currently build if you are using a later version of
the IAR tool chain. The issue is caused by changes to macro names within the compiler header files.


#### Silicon Labs SDCC ports

Unfortunately these will not work with the latest compiler versions. The compiler version used to generate the
port is now rather old, but is stated on the port documentation page.
