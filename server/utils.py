from server.scraper import Sitting


def chunk_data(sitting: Sitting):
    """
    Chunks data - tries to keep chunks around 400 words long and split at sentence endings if possible.
    """
    new_sittings = []

    chunk_number = 0
    chunk_length = 0
    chunk_array = sitting.text.split(" ")
    sitting_text = ""
    # If chunk is small, don't split
    if len(chunk_array) < 500:
        return [sitting]

    for word in chunk_array:
        sitting_text += f"{word} "
        chunk_length += 1
        if ( chunk_length > 400 and "." in word ) or chunk_length > 500:
            new_title = (
                sitting.title
                if chunk_number == 0
                else f"{sitting.title}({chunk_number})"
            )
            new_id = (
                sitting.meeting_id
                if chunk_number == 0
                else f"{sitting.meeting_id}({chunk_number})"
            )
            new_sittings.append(
                Sitting(new_id, new_title, sitting.date, sitting.link, sitting_text)
            )
            chunk_length = 0
            chunk_number += 1
            sitting_text = ""

    if sitting_text != "":
        new_title = (
            sitting.title if chunk_number == 0 else f"{sitting.title}({chunk_number})"
        )
        new_id = (
            sitting.meeting_id
            if chunk_number == 0
            else f"{sitting.meeting_id}({chunk_number})"
        )
        new_sittings.append(
            Sitting(new_id, new_title, sitting.date, sitting.link, sitting_text)
        )

    return new_sittings


if __name__ == "__main__":
    sitting = Sitting(
        "test",
        "test",
        "test",
        "test",
        """There is no strife, no prejudice, no national conflict in outer space as yet. Its hazards are hostile to us all. Its conquest deserves the best of all mankind, and its opportunity for peaceful cooperation many never come again. But why, some say, the moon? Why choose this as our goal? And they may well ask why climb the highest mountain? Why, 35 years ago, fly the Atlantic? Why does Rice play Texas?
We choose to go to the moon. We choose to go to the moon in this decade and do the other things, not because they are easy, but because they are hard, because that goal will serve to organize and measure the best of our energies and skills, because that challenge is one that we are willing to accept, one we are unwilling to postpone, and one which we intend to win, and the others, too.
It is for these reasons that I regard the decision last year to shift our efforts in space from low to high gear as among the most important decisions that will be made during my incumbency in the office of the Presidency.
In the last 24 hours we have seen facilities now being created for the greatest and most complex exploration in man's history. We have felt the ground shake and the air shattered by the testing of a Saturn C-1 booster rocket, many times as powerful as the Atlas which launched John Glenn, generating power equivalent to 10,000 automobiles with their accelerators on the floor. We have seen the site where the F-1 rocket engines, each one as powerful as all eight engines of the Saturn combined, will be clustered together to make the advanced Saturn missile, assembled in a new building to be built at Cape Canaveral as tall as a 48 story structure, as wide as a city block, and as long as two lengths of this field.
Spaceflight will never tolerate carelessness, incapacity, and neglect. Somewhere, somehow, we screwed up. It could have been in design, build, or test. Whatever it was, we should have caught it. We were too gung ho about the schedule and we locked out all of the problems we saw each day in our work.
“Every element of the program was in trouble and so were we. The simulators were not working, Mission Control was behind in virtually every area, and the flight and test procedures changed daily. Nothing we did had any shelf life. Not one of us stood up and said, ‘Dammit, stop!’ I don’t know what Thompson’s committee will find as the cause, but I know what I find. We are the cause! We were not ready! We did not do our job. We were rolling the dice, hoping that things would come together by launch day, when in our hearts we knew it would take a miracle. We were pushing the schedule and betting that the Cape would slip before we did.
“From this day forward, Flight Control will be known by two words: ‘Tough’ and ‘Competent.’ Tough means we are forever accountable for what we do or what we fail to do. We will never again compromise our responsibilities. Every time we walk into Mission Control we will know what we stand for. Competent means we will never take anything for granted. We will never be found short in our knowledge and in our skills. Mission Control will be perfect.
When you leave this meeting today you will go to your office and the first thing you will do there is to write ‘Tough and Competent’ on your blackboards. It will never be erased. Each day when you enter the room these words will remind you of the price paid by Grissom, White, and Chaffee. These words are the price of admission to the ranks of Mission Control.
""",
    )
    print(chunk_data(sitting))
