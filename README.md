# Digital Ocean Droplet Resize

This script was created to automatically resize a Digital Ocean droplet when being used concurrently in a classroom by multiple students. When class was not in session, the droplet did not need to be at expanded capacity.

```
Usage: do_resize.py [-h] [--resize [RESIZE]] [--expand] [--contract] [-v]

This script can resize a Digital Ocean droplet. It is intended to be used for
scheduling a droplet resize at a specific time using cron, but can be used at
any event trigger.

The following arguments can be used when executing the script

optional arguments:
  -h, --help         show this help message and exit
  --resize [RESIZE]  Specify the droplet size
  --expand           Expand to larger droplet
  --contract         Resize to smaller droplet
  -v, --verbose      Turn on output
```

## Requirements
This script is written for Python 3. It relies on Python 3 and three additional libraries that may require installation on your computer. They are:

* requests
* argparse
* json

The **time** and **sys** libraries should be installed by default with Python.


## Usage
Download this repository to the computer that will be running the cron job to resize the droplet. This can be any computer _except_ the target droplet.

Change the file permissions of do_resize.py to a+rx or 755 in order to allow the script to be executed.

Open the `config.json` file in a text editor. In that file there are five items that must be configured in order for the script to run properly.

**`apikey`** - this is the API key for your Digital Ocean account you'll need in order to issue the command to resize the droplet. Please refer to [https://www.digitalocean.com/docs/api/](https://www.digitalocean.com/docs/api/) for instructions on how to create an API key.

**`dropletID`** - this is the ID of the target droplet. To find the ID of the target droplet, click on the name of the droplet on the main droplet screen. In the URL of the droplet detail screen you will find the ID. In this example:

```https://cloud.digitalocean.com/droplets/12345678/graphs?i=xxxxxx```

the value **`12345678`** is the droplet ID.

**`url`** - This is the API URL for Digital Ocean. This value may change in the future. As of this writing, the value is `https://api.digitalocean.com/v2/droplets/` 

**`lgsize`** - this is the default expanded droplet size. It is set using the slug for the sizes available in the region where your droplet is located. The default is **s-4vcpu-8gb** For example, in the New York 1 region, the following droplet size slugs are valid:

*   "c-16"
*   "c-2"
*   "c-4"
*   "c-8"
*   "m-1vcpu-8gb"
*   "m-16gb"
*   "m-32gb"
*   "m-64gb"
*   "m-128gb"
*   "m-224gb"
*   "g-2vcpu-8gb"
*   "g-4vcpu-16gb"
*   "g-8vcpu-32gb"
*   "g-16vcpu-64gb"
*   "gd-2vcpu-8gb"
*   "gd-4vcpu-16gb"
*   "gd-8vcpu-32gb"
*   "gd-16vcpu-64gb"
*   "gd-32vcpu-128gb"
*   "512mb"
*   "1gb"
*   "2gb"
*   "4gb"
*   "8gb"
*   "16gb"
*   "32gb"
*   "48gb"
*   "64gb"
*   "s-1vcpu-1gb"
*   "s-3vcpu-1gb"
*   "s-1vcpu-2gb"
*   "s-2vcpu-2gb"
*   "s-1vcpu-3gb"
*   "s-2vcpu-4gb"
*   "s-4vcpu-8gb"
*   "s-6vcpu-16gb"
*   "s-8vcpu-32gb"
*   "s-12vcpu-48gb"
*   "s-16vcpu-64gb"
*   "s-20vcpu-96gb"
*   "s-24vcpu-128gb"
*   "gd-40vcpu-160gb"
*   "s-32vcpu-192gb"

**`smsize`** - this is the default contracted droplet size. It is set using the slug for the sizes available in the region where your droplet is located. The default size is **1gb**.


From the command line, issue the command `./do_resize.py --expand`. This will shut down the droplet, resize it, and restart it. If you include the `--resize [slug]` parameter, it will override the default contained in the `config.json` file.

Without any parameters set, the script will automatically reduce the droplet to the smaller size. The `--contract` parameter is available to explicitly state the behavior of the script.

By setting the `--verbose` parameter, the script will output some information regarding the stage of the script. By default, there is no output.

## TODO

1. Modify the script to accept all parameters from the command line. This will enable multiple droplets to be resized.
2. Modify the config.json to allow multiple droplets to be configured and resized.