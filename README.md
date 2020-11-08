# Hoarder
<p align="center">
<img alt="hoarder logo" src="https://github.com/muteb/Hoarder/blob/master/hoarder_logo.png" title="hoarder" height="25%" width="25%">
</p>
<p align="center">
Hoarder is a script made to collect and parse the most valuable artifacts for forensics or incident response investigations rather than imaging the whole hard drive, now it combined with <a href="https://github.com/AbdulRhmanAlfaifi/Rhaegal">Rhaegal</a> to add detection feature
</p>


## Introduction
To add easy of use and help analysts, we combined multiple tools in same repo., also the results stored in ```.kjson``` files, which can be pushed to Kuiper for visulization.
- Collection: [Hoarder](https://github.com/muteb/Hoarder)
- Parsing: [MasterParser](https://github.com/alwashmi/MasterParser)
- Detection: [Rhaegal](https://github.com/AbdulRhmanAlfaifi/Rhaegal)
- Visulization: [Kuiper](https://github.com/DFIRKuiper/Kuiper)

## Executable Releases:
You may find the latest windows binary release [here](https://github.com/muteb/Hoarder/releases/latest)

**Note on 32-bit release:** as of Hoarder 4.0.0, the 32-bit binary is no longer released. If you want to run hoarder in 32-bit endpoint, you can refer to the latest [32-bit release](https://github.com/muteb/Hoarder/releases/tag/3.2.0).

## Usage

### Collection

Hoarder parses the configuration `Hoarder.yml` and produces an extensive help message for ease of use.
```
.\hoarder.exe -h
usage: hoarder.exe [-h] [-V] [-v] [-vv] [-a] [-f IMAGE_FILE] [-pa] [-n] [-sp {1,2,3,4,5,6}] [-r] [-p] [-s] [--Events] [--Ntfs] [--Recent] [--Startup] [--SRUM] [--Firwall] [--CCM] [--WindowsIndexSearch]
                   [--Config] [--Ntuser] [--applications] [--usrclass] [--PowerShellHistory] [--RecycleBin] [--WMI] [--scheduled_task] [--BMC] [--prefetch] [--WMITraceLogs] [--BrowserHistory] [--WERFiles]
                   [--BitsAdmin] [--SystemInfo] [-g [GROUPS [GROUPS ...]]]

Hoarder 4.5.0 is a tool to collect and parse windows artifacts.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Print Hoarder version number
  -v, --verbose         Print details of hoarder message in console
  -vv, --very_verbose   Print more details (DEBUG) of hoarder message in console
  -a, --all             Get all (Default)
  -f IMAGE_FILE, --image_file IMAGE_FILE
                        Use disk image as data source instead of the live machine disk image
  -pa, --parse_artifacts
                        Parse artifacts
  -n, --no_raw_files    Only bring parsed output. Do not bring any raw evidence files
  -sp {1,2,3,4,5,6}, --set_priority {1,2,3,4,5,6}
                        Will run Hoarder process with the selected priority. 1: BELOW_NORMAL_PRIORITY_CLASS 2: IDLE_PRIORITY_CLASS (default) 3: NORMAL_PRIORITY_CLASS 4: ABOVE_NORMAL_PRIORITY_CLASS 5:
                        HIGH_PRIORITY_CLASS 6: REALTIME_PRIORITY_CLASS
  -r, --Rhaegal         Enable detection using Rhaegal rules, only possible if parsing enabled (-sp), default not enabled
  -g [GROUPS [GROUPS ...]], --groups [GROUPS [GROUPS ...]]
                        Specify what to collect by group tag. takes a space seperated list of groups. e.g. -g execution user_activities. Available groups: ['parsing']

Plugins:
  -p, --processes       Collect information about the running processes.
  -s, --services        Collect information about the system services.

Artifacts:
  --Events              Windows event logs
  --Ntfs                $MFT file
  --Recent              Recently opened files
  --Startup             Startup info
  --SRUM                SRUM folder
  --Firwall             Firewall Logs
  --CCM                 CCM Logs
  --WindowsIndexSearch  Windows Search artifacts
  --Config              System hives
  --Ntuser              All users hives
  --applications        Amcache files
  --usrclass            UserClass.dat file for all the users
  --PowerShellHistory   PowerShell history for all the users
  --RecycleBin          RecycleBin Files
  --WMI                 WMI OBJECTS.DATA file
  --scheduled_task      Scheduled Tasks files
  --BMC                 BMC files for all the users
  --prefetch            Prefetch files
  --WMITraceLogs        WMI Trace Logs
  --BrowserHistory      BrowserHistory Data
  --WERFiles            Windows Error Reporting Files
  --BitsAdmin           Bits Admin Database (QMGR database)

Commands:
  --SystemInfo          Get system information
```

### Examples

Let's say you want to collect all of the artifacts specified in `Hoarder.yml` then all you need to do is:

`> .\hoarder.exe --all` or `> .\hoarder.exe -a` or simply `> .\hoarder.exe` :).

After the script finishes, it will generate a zip file called `<HOSTNAME>.zip` containing all of the artifacts in addition to  `hoarder.log` that contains the script debugging logs (a JSON log will also be packaged in the `.zip` results).

To collect all artifacts with the group tag `parsing`, run the following command:
`> .\hoarder.exe -g parsing`

To run hoarder to collect Ntfs and Events artifacts, run the following command:
`> .\hoarder.exe --Ntfs --Events`

**Note:** you can combine multiple groups, multiple artifacts, or even groups and artifacts, and expect hoarder to come up with a unique set of all artifacts you want to collect.

## Configuration (Hoarder.yml)
Hoarder comes with the default configuration ```Hoarder.yml``` embedded in the release, if you want to use different configuration, modify the ```Hoarder.yml``` and re-combile it (check build binaries section). 
 1. **If you are running from the the binary executable:** `Hoarder.yml` default configuration is embedded in it. If you place your own `Hoarder.yml` next to `hoarder.exe` it will use it instead of the default configuration.
 2. **If you are running from source:** you can modify `Hoarder.yml` or rename it and name your own configuration `Hoarder.yml`.

### Add an Artifact to Hoarder.yml
*Tip: Refer to the default configuration for reference*
#### File and Folder Artifacts
The following is an example of file or folder collection and parsing:
```yaml
  Events: 
      output: 'Events'
      path32: '\windows\system32\winevt\Logs\'
      path64: '\windows\system32\winevt\Logs\'
      groups: 'parsing'
      files: '*'
      parsers: '<|parsingdir|>MasterParser.exe -p Events -i <|path|\> -o <|output|evtx.kjson>'
      description: 'Windows event logs'
```

* **Events** : This is the name of the artifact. This name will be used as an argument in the hoarder command line.
* **output** : This is the name of the output folder for this artifact.
* **path32** : The path to the artifact for 32bit systems, you can use \* as widecard, and ** as recursive.
* **path64** : The path to the artifact for 64bit systems, you can use \* as widecard, and ** as recursive.
* **files** : The file name/s. it could be a single string or a list as the example above, also you can use * as widecard.
* [Hoarder 4.0.0 and above] **groups:** groups are like tags and each artifact can be set to be part of one or more groups. In hoarder command line, one or more group(s) can be chosen and the artifacts tagged by this group will be used. If an artifact is chosen (e.g. --Ntfs) and a group is chosen (e.g. -g playbook), hoarder will process both.
* [Hoarder 4.0.0 and above] **parsers:** One or more parsers to run for this artifact.
	- It can be one parser. Example:
  
```yaml
    parsers: '<|parsingdir|>MasterParser.exe -p Events -i <|path|\> -o <|output|evtx.kjson>'
```
It can also be a list. Example:
	
```yaml
    parsers:
	- '<|parsingdir|>MasterParser.exe -p WMI_Persistence -i <|path|OBJECTS.DATA> -o <|output|WMI_Persistence.kjson>'
	- '<|parsingdir|>MasterParser.exe -p RUA -i <|path|OBJECTS.DATA> -o <|output|RUA.kjson>'
```
* **description** : a description about the artifact. This key is used in hoarder command line to show information about the artifact.


#### Parsers directives:
- `<|path|>`: e.g. `<|path|$MFT>` will be replaced with the path where any `$MFT` file under the artifact path exists, and a command will be run for each `$MFT` file found. To direct it to a folder it must end with `\`. Example: `<|path|\>` or `<|path|windows\>`.
- `<|output|>`: will be replaced with a unique output path to ensure no file is overwritten. `|output|` can be followed by a suffix (not a path - not ending in `\`) to be appended to all auto-generated filenames. For example, `<|output|evtx.json>` and the suffix `evtx.json` will be added to all windows events parsing output files. Tip: it is recommended to always use `<|output|>` to avoid writing results outside the working directory or overwriting outputs.
- `<|parsingdir|>`: this will be replaced with the path of the parsing working directory, where all files in parsers.zip are extracted, (WITH the trailing `\`). This directive doesn't take a suffix but you can append right after it. For example, if your parser takes in a rules folder in `parsers.zip`, you can refer to it as `<|parsingdir|>rules\`. This directive needs to go before any use of a tool or supplied input in `parsers.zip`.

## Parsing
Starting from hoarder 4.0.0, hoarder supports parsing collected artifacts. There are three major parts to parsing:
 1. **parsers.zip:** contains all of your parser binaries, scripts, and data files. Hoarder binary release comes prepackaged with MasterParser. To add your own parsers, place a `parsers.zip` next to `hoarder.exe` containing all of your parsers used. If you are running from source create your own `parsers.zip` and rename or delete the default `parsers.zip`.
 2. **configuration:** in Hoarder.yml, add your parser command (refer to [Add an Artifact to Hoarder.yml](#add-an-artifact-to-hoarderyml))
 3. **command-line arguments:** `-pa` to have hoarder bring both raw and parsed artifacts. `-n` to have hoarder bring only parsing results. Parsing arguments work with other switches as you would expect. Meaning, If a group or a single artifact is chosen, parsing will only be applied to the chosen artifacts.
 4. **Rhaegal rules:** `-r` this option enable running the detection on parsed results, if parsing not enabled, detection will not applied.
 
 
## Plugins and Commands:
- **Plugins**: predefined functions inside the script that can be called to get specific results, such as processes and services.
- **Commands**: defined inside `Hoarder.yml` to execute single built-in commands, such as `systeminfo`.

#### Command Execution 
Hoarder also support the execution of system commands. The following example shows the execution of the command "systeminfo":

```yaml
  SystemInfo:
    output: 'SystemInfo'
    cmd: 'systeminfo'
    description: 'Get system information'
```

* **SystemInfo** : This is the name of the command. This name will be used as an argument in the hoarder command line.

* **output** : This is the name of the output folder for the command results.

* **cmd** : The command to be executed.

* **description** : a description  about the artifact. This key is used in hoarder command line to show some information about the artifact.

## Running and freezing from source

### Environment


### Installing Dependencies

To install all Hoarder dependencies, run the following command from an elevated terminal:

`pip install -r requirements.txt` 

### compile the executable
Make sure your environment or virtual environment is setup with Python [3.8.5](https://www.python.org/downloads/release/python-385/)

To compile hoarder script, run :

```pyinstaller.exe hoarder.spec ```

To comipe MasterParser script, run:

```pyinstaller.exe MasterParser.spec```


Use the tool ```pyinstaller``` to compile the executable incase of the following

* **To add parser:**
Add parser to the folder ```parsers```, then combile MasterParser, then add ```MasterParser.exe``` to ```parsers.zip```, then compile Hoarder

* **To add rules:**
Add the rule to ```parsers.zip\rules.zip\```, then compile Hoarder

* **To data artifacts to collect:**
Add the artifacts to ```Hoarder.yml```, then compile Hoarder



### Freezing Hoarder into a binary
If you want to freeze your own binary make sure you install PyInstaller [3.6](https://www.pyinstaller.org/). You may need to change or add to this command if your changes contain [hidden imports](https://pyinstaller.readthedocs.io/en/stable/usage.html), [data files](https://pyinstaller.readthedocs.io/en/stable/usage.html), or [dll dependencies](https://pyinstaller.readthedocs.io/en/stable/usage.html) that PyInstaller needs to know about.

### Pull requests
Pull requests are welcome!
They will be tested then applied. We'll try to do some simple modifications if testing is not successful depending on the amount of modifications needed.

## License
This project is licensed under [GNU General Public License v3.0](https://github.com/muteb/Hoarder/blob/master/LICENSE)

## Related Projects
- Kuiper: https://github.com/DFIRKuiper/Kuiper

## Contributors:
This project built by the team (except some of the parsers).
- [Muteb Alqahtani](https://twitter.com/muteb_alqahtani)
- [Saleh Bin Muhaysin](https://twitter.com/saleh_muhaysin)
- [AbdulRhman Alfaifi](https://twitter.com/A__ALFAIFI)
- [Abdulaziz Alwashmi](https://twitter.com/AlwashmiA)
- [Abdullah Alrasheed](https://twitter.com/abdullah_rush)

