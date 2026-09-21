import re


def load_faq(filename="faq.txt"):
    faq = []

    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    for i in range(0, len(lines), 2):
        question = lines[i].removeprefix("Q:").strip()
        answer = lines[i + 1].removeprefix("A:").strip()
        faq.append((question, answer))

    return faq


def keywords(text):
    words = re.findall(r"[а-яёa-z0-9]+", text.lower())
    stop_words = {
        "а", "и", "в", "во", "на", "по", "с", "со",
        "к", "когда", "какой", "какие", "кто", "что",
        "это", "нужно", "будет", "ли"
    }
    return set(words) - stop_words


def find_answer(user_question, faq):
    user_words = keywords(user_question)

    best_answer = None
    best_score = 0

    for question, answer in faq:
        question_words = keywords(question)

        if not question_words:
            continue

        score = len(user_words & question_words) / len(question_words)

        if score > best_score:
            best_score = score
            best_answer = answer

    if best_score >= 0.4:
        return best_answer

    return "Не знаю."


def main():
    faq = load_faq()

    print("FAQ-бот. Напишите вопрос или 'выход'.")

    while True:
        user_question = input("> ").strip()

        if user_question.lower() in {"выход", "exit", "quit"}:
            break

        print(find_answer(user_question, faq))


if __name__ == "__main__":
    main()
