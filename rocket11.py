import collections
import os
import pathlib
import re
import requests
import shutil
import stat
import string
import subprocess
import traceback

class WimInfo:
    ImageInfo = collections.namedtuple('ImageInfo','index, name, description, size')
    def __init__(self,wim:pathlib.Path):
        run = subprocess.run(
            args=(
                'dism','/english',
                '/get-imageinfo',
                '/imagefile:'+str(wim),
            ),
            capture_output=True,
            text=True,
            check=True,
        )
        image_pattern = r'Index : (?P<index>\d*)\nName : (?P<name>.*)\nDescription : (?P<description>.*)\nSize : (?P<size>.*) bytes\n\n'
        wiminfo = re.fullmatch(
            pattern=r'\nDeployment Image Servicing and Management tool\nVersion: (?P<version>.*)\n\nDetails for image : (?P<path>.*)\n\n('+image_pattern+')*The operation completed successfully.\n',
            string=run.stdout,
            flags=re.MULTILINE,
        ).groupdict()
        self.version = wiminfo['version']
        self.path = pathlib.Path(wiminfo['path'])
        self.images = list()
        for imginfo in re.finditer(
            pattern=image_pattern,
            string=run.stdout,
            flags=re.MULTILINE,
        ):
            self.images.append(
                WimInfo.ImageInfo(**imginfo.groupdict())
            )
        assert self.path == wim
    def __repr__(self):
        return f'{self.__class__}(version={self.version!r},path={self.path!r},images={self.images!r})'

class WimMount:
    def __init__(self,wim:pathlib.Path,idx:int,mnt:pathlib.Path='mnt'):
        self.wim = pathlib.Path(wim)
        self.idx = int(idx)
        self.mnt = pathlib.Path(mnt)
    def __enter__(self):
        print(f'\n## Mounting {self.wim} {self.idx} to {self.mnt} ...')
        self.mnt.mkdir()
        subprocess.run(
            args=(
                'dism','/english',
                '/mount-image',
                '/imagefile:'+str(self.wim),
                '/index:'+str(self.idx),
                '/mountdir:'+str(self.mnt),
            ),
            # capture_output=True,
            # text=True,
            check=True,
        )
        print('mounted.')
        return self
    def __exit__(self,*exc):
        print(f'\n## Unmounting {self.wim} {self.idx} from {self.mnt} ...')
        subprocess.run(
            args=(
                'dism','/english',
                '/unmount-wim',
                '/mountdir:'+str(self.mnt),
                '/discard' if any(exc) else '/commit',
            ),
            # capture_output=True,
            # text=True,
            check=True,
        )
        self.mnt.rmdir()
        print('discarded.' if any(exc) else 'commited')

def provide_winget_package():
    print('\n## Providing winget package\n')
    base = pathlib.Path('winget')
    base.mkdir(exist_ok=True)
    with requests.Session() as session:
        latest=session.get(
            url='https://api.github.com/repos/microsoft/winget-cli/releases/latest'
        ).json()
        for asset in latest['assets']:
            name = asset['name']
            dst = base / name
            if dst.exists():
                print(f'{dst} found.')
            else:
                print(f'Downloading {dst} ...')
                with open(str(dst),'wb') as fdst:
                    shutil.copyfileobj(
                        fsrc=session.get(
                            url=asset['browser_download_url'],
                            stream=True,
                        ).raw,
                        fdst=fdst,
                    )
                if name.endswith('.zip'):
                    subprocess.check_call(
                        args=(
                            'powershell',
                            '-wd', str(base),
                            '-c', 'Expand-Archive',
                            '-Path', name,
                            '-Force',  # overwrite if exists
                        ),
                    )
    print('winget package available.')

def main():
    for letter in string.ascii_uppercase:
        wim_path = pathlib.WindowsPath(f'{letter}:/sources/install.wim')
        if wim_path.is_file(): break
    else:
        print('No drive with sources/install.wim found.')
        print('Did you insert a usb drive or mount a vhdx with windows installation media on it?')
        return -1
    print(f'Installation image found at {wim_path}')
    
    wim_info = WimInfo(wim_path)
    if not all(image.name.startswith('Windows 11') and image.description.startswith('Windows 11') for image in wim_info.images):
        print(f'{wim_path} does not look like a Windows 11 medium. Aborting.')
        return -2

    provide_winget_package()

    for image in wim_info.images:
        print(f'\n# Rocketizing {image.name}...\n')
        with WimMount(
            wim=wim_path,
            idx=image.index,
        ) as wim_mount:
            try:
                print('\n## Chamfering Edge...\n')
                for edge in (
                    list((wim_mount.mnt/'Program Files (x86)'/'Microsoft').glob('Edge*'))+
                    list((wim_mount.mnt/'Windows'/'WinSxS').glob('amd64_microsoft-edge-webview_31bf3856ad364e35*'))+
                    ([wim_mount.mnt/'Windows'/'System32'/'Microsoft-Edge-Webview'] if (wim_mount.mnt/'Windows'/'System32'/'Microsoft-Edge-Webview').exists() else [])
                ):
                    print(f'removing {edge}...')
                    shutil.rmtree(
                        path=edge,
                        onexc=lambda function,path,exception: (
                            subprocess.check_call(args=('takeown','/F',path)),  # todo : ux : reduce verbosity
                            subprocess.check_call(args=('icacls',path,'/grant',f"{os.environ['USERDOMAIN']}\\{os.environ['USERNAME']}:F")),  # todo : ux : reduce verbosity
                            os.chmod(path, stat.S_IWRITE),
                            function(path),
                        ) if pathlib.Path(path).exists() else None
                    )
                print('Edge chamfered.')

                print('\n## Detaching worldly demands...\n')
                run = subprocess.run(
                    args=(
                        'dism','/english',
                        '/get-capabilities',
                        '/image:'+str(wim_mount.mnt),
                    ),
                    capture_output=True,
                    text=True,
                    check=True,
                )
                capability_pattern = r'Capability Identity : (?P<id>.*)\nState : (?P<state>.*)\n\n'
                capabilites = re.fullmatch(
                    pattern=r'\nDeployment Image Servicing and Management tool\nVersion: (?P<version>.*)\n\nImage Version: (?P<img_version>.*)\n\nCapability listing:\n\n('+capability_pattern+')*The operation completed successfully.\n',
                    string=run.stdout,
                    flags=re.MULTILINE,
                ).groupdict()
                for capability in filter(
                    lambda p: (
                        p['state'] == 'Installed'
                        and not p['id'].startswith('Language.Basic')
                        and not p['id'].startswith('Microsoft.Windows.Ethernet.Client')
                        and not p['id'].startswith('Microsoft.Windows.PowerShell')
                        and not p['id'].startswith('Microsoft.Windows.Sense.Client')
                        and not p['id'].startswith('Microsoft.Windows.Wifi.Client')
                        and not p['id'].startswith('Windows.Client.ShellComponents')
                    ),
                    re.finditer(
                        pattern=capability_pattern,
                        string=run.stdout,
                        flags=re.MULTILINE,
                    ),
                ):
                    print(f'removing capability {capability['id']}...')
                    subprocess.run(  # todo : ux : reduce verbosity
                        args=(
                            'dism','/english',
                            '/remove-capability',
                            '/image:'+str(wim_mount.mnt),
                            '/capabilityname:'+capability['id']
                        ),
                        #capture_output=True,
                        #text=True,
                        check=True,
                    )
                print('Demands detached.')

                print('\n## Activating infinite potential...\n')
                subprocess.run(
                    args=[
                        'dism','/english',
                        '/add-provisionedappxpackage',
                        '/image:'+str(wim_mount.mnt),
                        '/packagepath:.\\winget\\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle',
                        '/licensepath:.\\winget\\e53e159d00e04f729cc2180cffd1c02e_License1.xml',
                        '/region:all',
                    ]+list('/dependencypackagepath:'+str(dep) for dep in pathlib.Path('./winget/DesktopAppInstaller_Dependencies/x64').glob('*.appx')),
                    #capture_output=True,
                    #text=True,
                    check=True,
                )
                print('Potential activated.')
            except:
                traceback.print_exc()
                input('press [enter] to continue...')  # stop here for interactive analysis of the faulty situation before unmounting and stuff
                raise
    print(f'\n{len(wim_info.images)} images rocketized.')
if __name__=='__main__': exit(main())
