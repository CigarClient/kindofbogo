from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__, template_folder='.')

def is_list_in_order(lst):
    for i in range(len(lst) - 1):
        if lst[i] >= lst[i + 1]:
            return False
    return True

def sort_numbers(numbers, delay):
    attempts = 0
    randomized_lists = []
    is_in_order = []

    while not is_list_in_order(numbers):
        attempts += 1
        print(f"Attempt {attempts}: The list is not in order. Randomizing the list...")
        random.shuffle(numbers)
        randomized_lists.append(numbers.copy())
        is_in_order.append(is_list_in_order(numbers))
        print("Randomized List:", numbers)
        time.sleep(int(delay) / 1000)

    result = {
        'attempts': attempts,
        'randomized_lists': randomized_lists,
        'is_in_order': is_in_order,
        'sorted_list': sorted(numbers)
    }
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort():
    delay = request.args.get('delay')

    # Check if the request contains a file
    if 'file' in request.files:
        file = request.files['file']
        numbers = [int(num.strip()) for num in file.read().decode('utf-8').split(',') if num.strip()]
    else:
        input_text = request.data.decode('utf-8')
        numbers = [int(num.strip()) for num in input_text.split(',') if num.strip()]

    result = sort_numbers(numbers, delay)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
