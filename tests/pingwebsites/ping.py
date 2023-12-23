def porthit():
    display_status_codes()
    
    while True:
        host = input("Enter the website URL to monitor (e.g., example.com): ")
        port = input("Enter the port to monitor (e.g., 80): ")

        last_status = None
        last_err = ''
        ping_count = 0
        
        try:
            while True:
                try:
                    start_time = datetime.now()
                    resp = requests.get(f"http://{host}:{port}", timeout=5)
                    end_time = datetime.now()

                    if resp.status_code != last_status:
                        print(f"{end_time.isoformat()}: Website is {resp.reason} ({resp.status_code})")
                        last_status = resp.status_code
                        last_err = ''
                    else:
                        print(f"{end_time.isoformat()}: Website status remains {resp.reason} ({resp.status_code})")
                    
                    ping_count += 1
                    if ping_count % 10 == 0:
                        decision = input("Do you want to continue? (Press Enter to continue, type 'stop' to halt scanning): ")
                        if decision.lower() == 'stop':
                            print("Monitoring stopped.")
                            return
                except Exception as e:
                    if str(e) != last_err:
                        print(f"{datetime.now().isoformat()}: Connection error ({str(e)})")
                        last_err = str(e)
                        last_status = None
                
                time.sleep(2)  # Wait for 2 seconds before the next ping

        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
            break

porthit()
