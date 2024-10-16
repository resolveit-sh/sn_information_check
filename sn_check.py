import os
import datetime
import csv

# Year codes 
year_codes = {
    '1': 2001, '2': 2002, '3': 2003, '4': 2004, '5': 2005, '6': 2006,
    '7': 2007, '8': 2008, '9': 2009, 'A': 2010, 'B': 2011, 'C': 2012,
    'D': 2013, 'E': 2014, 'F': 2015, 'G': 2016, 'H': 2017, 'J': 2018,
    'K': 2019, 'L': 2020, 'M': 2021, 'N': 2022, 'P': 2023, 'Q': 2024,
    'R': 2025, 'S': 2026, 'T': 2027, 'U': 2028, 'V': 2029, 'W': 2030,
    'X': 2031, 'Y': 2032
}

# Month codes 
month_codes = {
    '1': '01', '2': '02', '3': '03', '4': '04',
    '5': '05', '6': '06', '7': '07', '8': '08',
    '9': '09', 'A': '10', 'B': '11', 'C': '12'
}

# Hash database mapping
part_number_descriptions = {
    '02355FPJ': 'OceanStor Dorado 5600/5800/6000/6800 V6, STLZK8NVME7680, 7.68TB SSD NVMe Palm Disk Unit(7"), V22-H, HSSD',
    '02312YKR': 'Function Module, AC-DC PAC2000S12-B1, Server Platinum 2000W Version 2.0 AC power supply',
    '03059105': 'Finished Board Unit, PANGEA, STL6SPCBB22, Controller Module(Kunpeng920 96 Cores, 1*M.2, PALM, 100G Expansion board, 16*32GB, TPM Outside China'
    # Add more Part Numbers and Descriptions as needed
}

def is_valid_serial_number(sn):
    if len(sn) != 20:
        return False
    if sn[:2] != '21':
        return False
    year_code = sn[12].upper()
    month_code = sn[13].upper()
    if year_code not in year_codes:
        return False
    if month_code not in month_codes:
        return False
    return True

def get_serial_info(sn):
    vendor_pn = sn[2:10]
    year_code = sn[12].upper()
    month_code = sn[13].upper()
    year = year_codes[year_code]
    month = month_codes[month_code]
    return vendor_pn, year, month

def main():
    print("Log. Main function is running.")
    filename = input("Please input a filename path.\nBy default, it is set to ./sn_check.txt.\nYou can simply press Enter to use the default path.\n")

    if filename.strip() == '':
        filename = './sn_check.txt'

    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' does not exist.")
        exit(1)

    try:
        with open(filename, 'r') as file:
            serial_numbers = file.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        exit(1)

    results = []
    for idx, sn in enumerate(serial_numbers):
        sn = sn.strip()
        if not sn:
            continue  # Skip empty lines
        if sn.lower() == 'exit':
            break
        if not is_valid_serial_number(sn):
            print(f"Invalid Serial Number: {sn}")
            continue
        vendor_pn, year, month = get_serial_info(sn)
        description = part_number_descriptions.get(vendor_pn, 'N/A in internal database')
        month_year = f"{month}.{year}"
        # Output the information
        print("###########################################################")
        print(f"Serial Number: {sn}")
        print(f"Part Number: {vendor_pn}")
        print(f"Description: {description}")
        print(f"Month and Year of production: {month_year}")
        print("###########################################################\n")
        # Save to results
        results.append({
            'N': idx + 1,
            'Serial Number': sn,
            'Part Number': vendor_pn,
            'Description': description,
            'Month and Year of production': month_year
        })

    if results:
        now = datetime.datetime.now()
        filename_csv = now.strftime("SN_info_%Y%m%d_%H_%M_%S.csv")
        try:
            with open(filename_csv, 'w', newline='') as csvfile:
                fieldnames = ['N', 'Serial Number', 'Part Number', 'Description', 'Month and Year of production']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for data in results:
                    writer.writerow(data)
            print(f"Information saved to {filename_csv}")
        except Exception as e:
            print(f"Error writing to CSV file: {e}")
    else:
        print("No valid serial numbers were processed.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
