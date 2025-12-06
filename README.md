# 🚀 Rocket 11

A minimalist Windows 11 remix that launches your perfect system from *PowerShell* and *winget*.

## ⚙️ Usage

1. Get a Windows installation ISO of your choice. *(Windows 11 IoT Enterprise LTSC for best results)*
2. Create a USB installation medium using [Rufus](https://rufus.ie) or any working alternative. *(If you want or need a virtual medium, create and attach a vhdx using Windows' disk manager. Rufus will recognize and write to it.)*
3. Run 🚀 Rocket 11
   ```bash
   winget install Git.Git  # if you don't have Git yet; restarting PowerShell may be required
   git clone https://github.com/MaykGyver/rocket11.git && cd rocket11  # get and enter the 🚀 Rocket 11 experience
   winget install Python.Python.3.13  # if you don't have a recent Python yet; restarting PowerShell may be required
   pip install pipenv  # if pipenv isn't installed yet; restarting PowerShell may be required
   pipenv update  # sets up the Python virtual environment for rocket11.py from Pipfile
   pipenv run python rocket11.py  # runs 🚀 Rocket 11 in its virtual environment; modifies the installation medium from step 2 for step 4
   ```
4. Use the modified installation medium on a new device.
5. Await updates.
6. Use *PowerShell* and *winget* on the new device to configure your ideal system.

## 🤔 Why?

In capitalism, it's common for products to become bloated—packed with features and components that are not only unwanted but can also waste resources in ways that negatively affect users in multiple aspects and ways. 🚀 Rocket 11 embraces minimalism not just to save RAM or disk space, but to reduce jitter in real-time applications and unlock the full performance your machine was built to deliver.

* Want a sleek and snappy workstation?
* Seeking more consistent aiming in your favorite FPS?
* Need a reliable real-time audio workstation for live performances?
* Working with embedded devices, machinery, or robotics?
* Exploring technological frontiers and hackplay?

🚀 Rocket 11 is here to make your computing experience sharper and more enjoyable.

## 🧠 Design and Basic Assumptions

Any deviation from the following principles is considered a bug in 🚀 Rocket 11. Reported issues must reference at least one of these principles to be evaluated. Requests promoting unethical or abusive use will be ignored or canceled, with brief reference to this policy.

### Integrity

Safe and secure operation takes priority. The original vendor's measures must remain intact unless the modifications are concisely designed, reflect the recognized rules of technology, and are equally effective.

### Minimalism

If a component or feature can be added post-installation without compromise in safety or security, then it should not be included in the installation medium or any default setup. A PowerShell statement or script that installs the feature on a replicable 🚀 Rocket 11 system is the perfect proof of minimalism.

### Legitimacy

This project does not endorse or support copyright violations or software piracy. If any conflicts arise related to this project, please file an issue so we can investigate and implement appropriate, reasonable measures.

## 🧭 Roadmap

Some user apps reinstall during the post-install update phase (Edge, DevHome, some more). It's easy to remove them manually (at least it's possible at all), but an automated approach would be nicer.

How do we assist casual users in finding and installing the perfect set of packages for their scenario? Community discussion welcome!

When 🚀 Rocket 11 matured and multiple users reported succesful use, we will fork it and start 🚀 Rocket 11.
