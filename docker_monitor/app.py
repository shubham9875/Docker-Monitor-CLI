import argparse
import docker

client = docker.from_env()

def list_containers():
    containers = client.containers.list(all=True)
    if not containers:
        print("No containers found.")
    for c in containers:
        print(f"{c.name}: {c.status}")

def check_status(required_containers):
    all_containers = {c.name: c.status for c in client.containers.list(all=True)}
    for rc in required_containers:
        status = all_containers.get(rc, "not found")
        print(f"{rc}: {status}")

def restart_failed():
    containers = client.containers.list(all=True)
    for c in containers:
        if c.status != "running":
            print(f"Restarting {c.name}...")
            c.restart()

def main():
    parser = argparse.ArgumentParser(description="DockerMonitor CLI - Monitor Docker containers")
    parser.add_argument("command", choices=["list", "check", "restart"], help="Command to run")
    parser.add_argument("--required", nargs="*", help="List of required containers for 'check'")
    args = parser.parse_args()

    if args.command == "list":
        list_containers()
    elif args.command == "check":
        if not args.required:
            print("Please specify --required container names")
        else:
            check_status(args.required)
    elif args.command == "restart":
        restart_failed()

if __name__ == "__main__":
    main()
