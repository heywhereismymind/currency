from django.views import View
from django.http import JsonResponse
from .models import CurrencyRate
import requests
import logging
import zlib
import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LoadDataView(View):
    def get(self, request):
        date = request.GET.get("date")

        if not date:
            return JsonResponse({"error": "Must be date in fromat YYYY-MM-DD"})

        response = requests.get(
            f"https://www.nbrb.by/api/exrates/rates?ondate={date}&periodicity=0"
        )

        if response.status_code == 200:
            data = response.json()
            result = []

            for i in data:
                i["date"] = datetime.datetime.strptime(
                    i.get("Date"), "%Y-%m-%dT%H:%M:%S"
                ).strftime("%Y-%m-%d")
                i["cur_code"] = i.get("Cur_ID")
                i["cur_official_rate"] = i.get("Cur_OfficialRate")
                del i["Cur_ID"]
                del i["Date"]
                del i["Cur_Abbreviation"]
                del i["Cur_Scale"]
                del i["Cur_Name"]
                del i["Cur_OfficialRate"]
                result.append(i)

            for item in result:
                CurrencyRate.objects.update_or_create(**item)

            crc32 = zlib.crc32(response.content)
            response = JsonResponse({"status": "success"})
            response["CRC32"] = crc32
            logger.info(f"Request: {request}, Response: {response}")
            return response

        return JsonResponse({{"error": "Cant get currency from NBRB.by"}})


class GetRateView(View):
    def get(self, request):
        date = request.GET.get("date")
        cur_code = request.GET.get("cur_code")

        if not date and cur_code:
            return JsonResponse(
                {
                    "error": "Must be date in fromat YYYY-MM-DD and Currency Code in format: ***"
                }
            )

        response = requests.get(
            f"https://www.nbrb.by/api/exrates/rates/{cur_code}?ondate={date}"
        )

        if response.status_code == 200:
            data = response.json()
            prev_date = datetime.datetime.strptime(
                date, "%Y-%m-%d"
            ) - datetime.timedelta(days=1)
            prev_response = requests.get(
                f'https://www.nbrb.by/api/exrates/rates/{cur_code}?ondate={prev_date.strftime("%Y-%m-%d")}'
            )

            if prev_response.status_code == 200:
                pred_data = prev_response.json()
                change = (
                    "increased"
                    if data.get("Cur_OfficialRate") > pred_data.get("Cur_OfficialRate")
                    else "decreased"
                )
                response_data = {
                    "date": date,
                    "cur_code": cur_code,
                    "rate": data.get("Cur_OfficialRate"),
                    "change": change,
                }
                response = JsonResponse(response_data)
                crc32 = zlib.crc32(str(response_data).encode())
                response["CRC32"] = crc32
                logger.info(f"Request: {request}, Response: {response}")
                return response

        return JsonResponse({"error": "Cant get currency from NBRB.by"})
