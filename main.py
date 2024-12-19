import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# 책 제목을 입력받는 함수 추가
def get_book_info(book_title):
    search_url = f'https://www.yes24.com/product/search?query={book_title}'
    data = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # print(search_url)

    # 첫 번째 책의 링크를 찾기
    first_book = soup.select_one('.info_name .gd_name')  # 첫 번째 책의 링크 선택
    if first_book:
        book_link = first_book['href']  # 책 링크 가져오기
        # book_link가 절대 경로가 아닐 경우, 기본 URL을 추가
        if not book_link.startswith('http'):
            book_link = 'https://www.yes24.com' + book_link  # 기본 URL 추가
        book_data = requests.get(book_link, headers=headers)
        book_soup = BeautifulSoup(book_data.text, 'html.parser')

        # 출판사 서평 추출
        review_element = book_soup.select_one('#infoset_pubReivew .infoSetCont_wrap .infoWrap_txt')
        if review_element:  # review_element가 None이 아닐 경우에만 접근
            review = review_element.get_text(separator="\n").strip()  # 텍스트 가져오기
        else:
            review = "서평을 찾을 수 없습니다."  # 서평이 없을 경우 기본 메시지

        return {
            'review': review  # 출판사 서평
        }
    return None

# 책 제목을 입력받고 정보 출력
book_title = input("책 제목을 입력하세요: ")
book_info = get_book_info(book_title)
if book_info:
    print(book_info)
else:
    print("책 정보를 찾을 수 없습니다.")