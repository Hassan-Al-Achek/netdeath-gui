import nmap3


class Scan:

    def __init__(self, target):
        self.target = target
        self.nm = nmap3.Nmap()

    def scan_top_ports(self):
        return self.nm.scan_top_ports(self.target)

    def services_version_detection(self):
        return self.nm.nmap_version_detection(self.target)

    def get_live_hosts(self):
        return self.nm.nmap_list_scan(self.target)


# if __name__ == '__main__':
#     scanner = Scan('10.0.2.115')
#     print(scanner.scan_top_ports())
    # print("")
    # print(scanner.services_version_detection())
    # print(scanner.get_live_hosts())
