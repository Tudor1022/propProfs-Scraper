from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import undetected_chromedriver as uchr


def scrape_proprofs_quiz(url, noQ, counter):
    #calculates how much time will it take
    print(f'Estimated time {noQ*16/60} minutes')
    print(f'Questions remaining {noQ}')
    driver = uchr.Chrome(headless=False,use_subprocess=False)
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,"p.fc-button-label").click()
    time.sleep(2)
    #starts the quiz and scrolls to make sure that the button is visible
    start_button = driver.find_element(By.CSS_SELECTOR, 'button.btn_class')
    driver.execute_script("arguments[0].scrollIntoView();", start_button)
    start_button.click()

    time.sleep(2)

    questions = []

    while counter<noQ:
        time.sleep(3)
        question_text = driver.find_element(By.CSS_SELECTOR, 'div.quiz_tablediv').text.strip()

        image_element = driver.find_elements(By.CSS_SELECTOR, 'div.ques_img_placeholder img')
        image_url = image_element[0].get_attribute('src') if image_element else None

        choices = []
        choice_elements = driver.find_elements(By.CSS_SELECTOR, 'div.answer_boxes')

        for choice_element in choice_elements:
            choice_text = choice_element.text.strip()
            choices.append(choice_text)

        questions.append({
            'question': question_text,
            'choices': choices,
            'image': image_url
        })

        try:
            #does the steps required to proceed to the enxt question
            choice_button=driver.find_element(By.CSS_SELECTOR, 'label.labelHover')
            driver.execute_script("arguments[0].scrollIntoView();", choice_button)
            time.sleep(2)
            choice_button.click()
            time.sleep(2)
            submit_button = driver.find_element(By.CSS_SELECTOR, 'div.btn_class')
            driver.execute_script("arguments[0].scrollIntoView();", submit_button)
            time.sleep(2)
            submit_button.click()
            time.sleep(2)  # Wait for the next question to load
            next_button = driver.find_elements(By.CSS_SELECTOR, 'div.btn_class')
            driver.execute_script("arguments[0].scrollIntoView();", next_button[len(next_button)-1])
            time.sleep(2)
            next_button[len(next_button)-1].click()
            counter=counter+1


        except Exception as e:
            print(e)

            break  #if no next button, edn the loop, and the quiz


    quiz_data = {
        'title': driver.title,
        'questions': questions
    }

    return quiz_data


def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Quiz saved to {filename}")


if __name__ == "__main__":
    quiz_url = input("Add the link to the quiz: ")
    q_numb=input("Add the question number: ")
    numb=int(q_numb)
    quiz_data = scrape_proprofs_quiz(quiz_url, numb,0)

    if quiz_data:
        save_to_json(quiz_data, "quiz1.json")
