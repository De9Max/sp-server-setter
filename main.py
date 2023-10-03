import os
import xml.etree.ElementTree as ET


cpu_modes = [("mode", 'custom'), ("match", 'exact'), ("check", 'partial')]
cpu_setts = [ET.fromstring("<model fallback='allow'>Westmere</model>"),
             ET.fromstring("<feature policy='disable' name='hypervisor'/>"),
             ET.fromstring("<feature policy='require' name='vmx'/>")]


def get_xml_files():
    files = os.listdir('/etc/libvirt/qemu')
    results = []
    for file in files:
        if "xml" in file:
            results.append(file)
    return results


def modify_xml(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    features = root.find("features")
    child_hyperv = ET.Element("hyperv")
    synic = ET.Element("synic")
    synic.set("state", "on")
    child_hyperv.append(synic)
    features.append(child_hyperv)
    cpu = root.find("cpu")
    for mode in cpu_modes:
        cpu.set(mode[0], mode[1])
    for setting in cpu_setts:
        cpu.append(setting)
    tree.write(file_name)


def set_kvm_intel():
    with open("/etc/modprobe.d/kvm.conf","w") as f:
        f.write("options kvm_intel nested=1")
    f.close()

def shutdown_vms(files):
    for vm in files:
        vm = vm.replace(".xml","")
        os.system(f"virsh shutdown {vm}")

def main():
    set_kvm_intel()
    xml_files = get_xml_files()
    shutdown_vms(xml_files)
    print(xml_files)
    for file in xml_files:
        modify_xml("/etc/libvirt/qemu/" + file)

    print("The end!")


if __name__ == '__main__':
    main()
