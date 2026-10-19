
import requests

year = 2026
courseLevel = "UG"
courseCategory = "BA"
semesterInRoman = "IV"

#university roll Replace xxx with appropriate number
startingUniversityRoll = "2520141070XXX"

#sets how many next result to download
#from given universtiy roll
rollCount = 10

rollWidth = len(startingUniversityRoll)

for rollOffset in range(rollCount):
    universityRoll = str(
        int(startingUniversityRoll) + rollOffset
    ).zfill(rollWidth)
    ppuPdfLink = (
        f"https://lu.indiaexaminfo.co.in/PATLIPUTRA/YEAR-{year}/"
        f"{courseLevel}/{courseCategory}(SEM-{semesterInRoman})/"
        f"{universityRoll}.pdf"
    )

    response = None
    try:
        response = requests.get(ppuPdfLink, stream=True, timeout=30)
        if response.status_code == 404:
            print(f"\nNo PDF found for roll {universityRoll}; skipping.")
            continue
        response.raise_for_status()

        pdfSize = response.headers.get("Content-Length")

        if pdfSize:
            print(f"\nRoll {universityRoll} - PDF Size: {int(pdfSize) / 1024:.2f} KB")
        else:
            print(f"\nRoll {universityRoll} - PDF size is unknown.")

        bytesDownloaded = 0
        with open(f"{universityRoll}.pdf", "wb") as fileObject:
            for chunk in response.iter_content(chunk_size=1024):
                if not chunk:
                    continue
                fileObject.write(chunk)
                bytesDownloaded += len(chunk)
                if pdfSize:
                    print(
                        f"\rDownloaded: {bytesDownloaded / 1024:.2f}/"
                        f"{int(pdfSize) / 1024:.2f} KB",
                        end="",
                        flush=True,
                    )
                else:
                    print(
                        f"\rDownloaded: {bytesDownloaded / 1024:.2f} KB",
                        end="",
                        flush=True,
                    )

        print(f"\nRoll {universityRoll}: PDF downloaded successfully.")
    except requests.RequestException as error:
        print(f"\nRoll {universityRoll}: download failed ({error}); skipping.")
    finally:
        if response is not None:
            response.close()
