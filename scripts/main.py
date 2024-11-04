from bs4 import BeautifulSoup
import pandas as pd
import requests

from class_ids import *


def get_value(element, tag, class_element, default="Unknown"):
    result = element.find(tag, {"class": class_element})
    if result:
        return result.text.strip()
    return default


def creating_df():

    start_page_no = 1

    max_page = 41

    df = pd.DataFrame()

    for curr_page_no in range(start_page_no, max_page + 1):
        url = "http://www.flipkart.com/search?q=mobiles&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=2&as-type=HISTORY&as-backfill=on"

        url_with_page_no = f"{url}&page={curr_page_no}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Referer": "https://www.google.com",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        page_data = requests.get(url_with_page_no, headers=headers)

        soup = BeautifulSoup(page_data.content, "html.parser")

        every_phone = soup.findAll("div", {"class": class_all_data})

        every_phone_data = []

        for phone in every_phone:

            phone_name = get_value(phone, "div", class_phone_name)

            rating = get_value(phone, "div", class_rating)

            phone_price = get_value(phone, "div", class_phone_price)

            phone_original_price = get_value(phone, "div", class_phone_original_price)

            phone_discount = get_value(phone, "div", class_phone_discount)

            specs = get_value(phone, "div", class_specs)

            no_rating_review = get_value(phone, "span", class_no_rating_review)
            no_review = "Unknown"
            no_rating = "Unknown"

            if no_rating_review != "Unknown":
                no_rating_review = no_rating_review.split("&")
                no_rating = no_rating_review[0]
                no_review = no_rating_review[1]

            find_image = phone.find("div", {"class": class_image})
            image_src = "Unknown"

            if find_image:
                image_src = find_image.img.get("src")

            find_assured = phone.find("div", {"class": class_assured})
            assured = False

            if find_assured:
                assured = True

            phone_data = [
                phone_name,
                rating,
                phone_price,
                no_rating,
                no_review,
                phone_original_price,
                phone_discount,
                assured,
                specs,
                image_src,
            ]
            every_phone_data.append(phone_data)

        columns = [
            "phone_name",
            "rating",
            "phone_price",
            "no_of_rating",
            "no_of_review",
            "original_price",
            "discount",
            "flipkart_assured",
            "specs",
            "image_src",
        ]
        df_new = pd.DataFrame(every_phone_data, columns=columns)
        df = pd.concat([df, df_new])

    return df


def saving(df, name):
    df.to_csv(f"data/{name}.csv", index=0)


def main():
    df = creating_df()
    saving(df, "result_finalized")


if __name__ == "__main__":
    main()
