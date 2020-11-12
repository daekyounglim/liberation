import sys
import os
import json
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('../..'))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('..'))))
from ExcelFileReader import ExcelFileReader


class NaverCrawlerCurl:

    def _get_json_data_(self, curl_command):
        curl_command = curl_command.replace("\n", "")
        curl_command = curl_command.replace("\\", "")
        result = subprocess.check_output(curl_command, shell=True)
        result = result.decode('utf-8')
        json_obj = json.loads(result)
        return json_obj

    def _read_template_(self):
        data = ExcelFileReader.load('../../data/naver_url.pkl')
        curl_list = []
        for row in data.values:
            pid = row[0]
            ncurl_pg = row[12]  # P&G Product curl url
            curl_list.append([pid, ncurl_pg])
        return curl_list

    def __parse_json__obj__(self, json_obj):
        """
        To-do : Json object를 파싱해서 dataframe로 만든다.
        """

    def __insert_data__(self, dataframee):

        """
        To-do : dataframe 을 테이블에 저장한다.
        """

    def process(self):
        curl_list = self._read_template_()
        for pid, curl in curl_list[:1]:  #excel template이 완성되면 제거할것.
            json = self._get_json_data_(curl)
            print(json)
            #df = self.__parse_json__obj__(json)
            #self.__insert_data__(df)

if __name__ == '__main__':
    naver = NaverCrawlerCurl()
    naver.process()

