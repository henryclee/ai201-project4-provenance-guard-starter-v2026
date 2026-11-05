"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "human-written samples",
        "criterion": 1,
        # Human written samples
        # Provenance:
        # 1–2	Personal narrative / reflective	NYT Tiny Memoir Contest winners
        # 3	Personal reflective	NYT Tiny Love Stories
        # 4	Personal, quirky	Washington Post “Life Is Short”
        # 5	Personal expressive (journal)	A Story Nerd’s Life blog
        # 6	Casual, typo-heavy	Reddit comment thread
        # 7	Academic reflective	College Board AP English Language teacher guide (student essay excerpt)
        # 8	Academic literary	Mark Twain, Life on the Mississippi, “Reading the River”
        # 9	Professional	University of Washington graduate-inquiry email sample
        # 10	Argumentative / persuasive	Holt “One Hundred Trees, Please” student model essay
        "texts": [
            "I fidgeted in the car, adjusting my SWAT gear. We parked, ready for a sugar raid. Dad shut the car door too soon. Bam! Part of my finger went with it. The back seat turned into triage. Mom tore off her Viking beard, wrapping it tight around my finger. My sisters cried as if they lost their fingers. Dad searched the car for my fingertip, nothing. Relief settled in on the way back from the E.R. It would heal, the doctor said. Two years later, the car has new owners. If they find what we failed to … well, happy Halloween.",
            "Your Christmas gift to me sits unopened on my desk, next to the one I wrapped for you. We joked about forgetting to exchange them, promising we'd “definitely remember next time.” Your mom mailed yours to me after the funeral. Some nights I sit and stare at them. Two little boxes, a tiny museum of the life we were supposed to keep living together. I think, Open it. Go. Do something. My hands stay still. It feels like once I tear the tape, our friendship will collapse into a moment in time. So the gifts stay closed. You stay close.",
            "A close friend died in 1999. After her funeral, grief's full weight incapacitated me. My boyfriend led me into our cramped apartment bathroom and pushed back the plastic curtain on the claw foot tub. I sank into near-scalding water and sobbed out my deep sadness while he silently massaged my arms and back with salt scrub. The grit made my skin raw, then cool and alive. Nearly three decades later, with both our marriage and divorce behind us, we pull from the same well of tenderness to co-parent our three daughters. Where love once was, its roots remain.",
            "Finally, a succinct summary of my life, courtesy of the Scholarships Experts Web site search form: Student does not have a car. Student has no dependents. Student has not been charged with or convicted of any misdemeanors or felonies. Student is drug-free. Student is non-violent. Student is right-handed. Student's parents are married. Student's sexual orientation: heterosexual. Student attended a high school within the immediate delivery area for Papa John's Pizza. I may not find that scholarship for graduate school, but I'm closer to a real understanding of who I am. A candidate for the National Right-Handed Carless Orderer-of-Papa-John's Award.",
            "Dear Journal, It is five minutes until midnight on Friday. We are having THE MOST TERRIFIC storm! Skull shattering deep rumbles, a non-stopping barrage of heavy raindrops, lightning that flashes the whole dark night back into daytime again. It is wondrous. Marvelous. Powerful. Makes my heart jump. But not just from adrenaline or fear, but also from something further down that makes me want to go out and be a part of it. Everything about its genius and miraculous power and beautiful presence shouts loudly “Pay attention. God is fantastic and creative and loves making beauty!” A witness.",
            "My high school had 4 guidance counselors. 3 were competent at their jobs. Mine opened the top draw of his desk and had a rotisserie chicken in it which he then proceeded to eat while attempting to explain why choosing a college is important. I'm not sure what I took away from that experience. Always expect a rotisserie chicken, I guess. At least he put the food under his own hat, rather than someone else's, UNLIKE Poodley P. McFustercluck: I remember a time when an honest dawg could bring in an entire rotisserie chicken to the theater without needing to hide it under his comically oversized cowboy hat. WE USED TO BE A COUNTRY!!! we used to wear parachute pants.",
            "In looking at mine, I become aware that it is so recent in the stretch of man's history that we have been able to stop time in this way and hold still for reflection. Vermeer is one of my favorite painters because of that sense of suspended time, with both clock and calendar held so wonderfully, so terribly still. The people in the snapshots are all strangers. My parents young, caught before I arrived or as they were when I saw them as towering grown-ups. They seemed so old then and so young now. And I am, to me, the strangest of all.",
            "It turned out to be true. The face of the water, in time, became a wonderful book—a book that was a dead language to the uneducated passenger, but which told its mind to me without reserve, delivering its most cherished secrets as clearly as if it uttered them with a voice. And it was not a book to be read once and thrown aside, for it had a new story to tell every day. Throughout Chapter 3 the long twelve hundred miles there was never a page that was void of interest, never one that you could leave unread without loss, never one that you would want to skip.",
            "Dear Dr. Huntington, My name is Georgina Geo, and I am writing to inquire about opportunities for graduate study in your group at the University of Washington. I am a recent graduate of the Department of Earth Sciences at Superstar University, where I had the opportunity to contact geochemistry research in the stable isotopes lab of Prof. Smartpants. I wanted to contact you to see if you were planning to accept students for the Fall of 201X. If so, do you have a sense for the types of projects that might be available to your students? I have read with interest the project descriptions on your web page and I am especially interested in potential projects involving geochemistry and the evolution of mountain systems and landscapes. I have attached a resume, and I would be happy to find any questions you might have about my background and experience. I look forward to hearing from you.",
            "As you probably know, the paper we use for our schoolwork and notes to our friends is made from trees. To this, some might say, “So what? Paper must be cheap, since it grows on trees.” True, in a way paper does grow on trees and is inexpensive. However, the environmental cost of making new paper is quite high. We should start a paper-recycling program here at our school if we are truly serious about helping the environment and ourselves. A paper-recycling program can help conserve our forests—forests filled with vital oxygen-producing trees. By decreasing our demand for trees, we can make a difference right here at our school. A ton of paper made from recycled material saves approximately seventeen trees.",
        ],
    },
    {
        "name": "ai and human samples",
        "criterion": 2,
        # 5 human samples, 5 ai samples
        # Provenance:
        # 1 Personnal narrative / reflective	NYT Tiny Memoir Contest winners
        # 2	Casual, typo-heavy	Reddit comment thread
        # 3	Academic literary	Mark Twain, Life on the Mississippi, “Reading the River”
        # 4	Professional	University of Washington graduate-inquiry email sample
        # 5	Argumentative / persuasive	Holt “One Hundred Trees, Please” student model essay
        "texts": [
            "I fidgeted in the car, adjusting my SWAT gear. We parked, ready for a sugar raid. Dad shut the car door too soon. Bam! Part of my finger went with it. The back seat turned into triage. Mom tore off her Viking beard, wrapping it tight around my finger. My sisters cried as if they lost their fingers. Dad searched the car for my fingertip, nothing. Relief settled in on the way back from the E.R. It would heal, the doctor said. Two years later, the car has new owners. If they find what we failed to … well, happy Halloween.",
            "My high school had 4 guidance counselors. 3 were competent at their jobs. Mine opened the top draw of his desk and had a rotisserie chicken in it which he then proceeded to eat while attempting to explain why choosing a college is important. I'm not sure what I took away from that experience. Always expect a rotisserie chicken, I guess. At least he put the food under his own hat, rather than someone else's, UNLIKE Poodley P. McFustercluck: I remember a time when an honest dawg could bring in an entire rotisserie chicken to the theater without needing to hide it under his comically oversized cowboy hat. WE USED TO BE A COUNTRY!!! we used to wear parachute pants.",
            "It turned out to be true. The face of the water, in time, became a wonderful book—a book that was a dead language to the uneducated passenger, but which told its mind to me without reserve, delivering its most cherished secrets as clearly as if it uttered them with a voice. And it was not a book to be read once and thrown aside, for it had a new story to tell every day. Throughout Chapter 3 the long twelve hundred miles there was never a page that was void of interest, never one that you could leave unread without loss, never one that you would want to skip.",
            "Dear Dr. Huntington, My name is Georgina Geo, and I am writing to inquire about opportunities for graduate study in your group at the University of Washington. I am a recent graduate of the Department of Earth Sciences at Superstar University, where I had the opportunity to contact geochemistry research in the stable isotopes lab of Prof. Smartpants. I wanted to contact you to see if you were planning to accept students for the Fall of 201X. If so, do you have a sense for the types of projects that might be available to your students? I have read with interest the project descriptions on your web page and I am especially interested in potential projects involving geochemistry and the evolution of mountain systems and landscapes. I have attached a resume, and I would be happy to find any questions you might have about my background and experience. I look forward to hearing from you.",
            "As you probably know, the paper we use for our schoolwork and notes to our friends is made from trees. To this, some might say, “So what? Paper must be cheap, since it grows on trees.” True, in a way paper does grow on trees and is inexpensive. However, the environmental cost of making new paper is quite high. We should start a paper-recycling program here at our school if we are truly serious about helping the environment and ourselves. A paper-recycling program can help conserve our forests—forests filled with vital oxygen-producing trees. By decreasing our demand for trees, we can make a difference right here at our school. A ton of paper made from recycled material saves approximately seventeen trees.",
            # AI generated samples by deepseek free tier
            "When I was twelve I broke my wrist trying to prove I could jump a fence in one motion. I remember the sound more than the pain — a clean snap that seemed to come from somewhere outside my body. My friend Ben ran to get his mother while I sat in the grass staring at my arm, which had developed a second elbow. The emergency room took four hours. The doctor asked how it happened, and I said skateboarding, because it sounded less stupid than the truth. My mother didn't correct me. She just looked at me the way she did when she was deciding whether to laugh.",
            "Genuinely cannot believe my school decided the best time to renovate the library was the three weeks before finals. There's a jackhammer going from 7am. 7am. I have a paper due Friday and my options are: study in the hall where a guy is screaming into his phone about a group project, or study in the cafeteria where they're playing the same five songs on a loop. I tried the library anyway and a guy in a hard hat told me I couldn't be there, which like, fair, but also it's literally called the library. Anyway I'm writing this from my car. It's 88 degrees. I have four more hours of this.",
            "In The Yellow Wallpaper, Gilman never lets the narrator name her own condition, which is precisely the point. She describes the wallpaper in obsessive detail — the pattern that plunges off at a wild angle, the woman creeping behind it — while the vocabulary that would explain her situation is withheld. What struck me on a second reading is how the story's horror is structural rather than emotional. The prose stays calm, almost domestic, even as the narrator's world narrows to a single room. Gilman's achievement is that the reader notices the walls closing before the narrator does, and that discomfort becomes part of the story's argument.",
            "Dear Professor Nakamura, I am writing to ask whether you are accepting new graduate students for the fall 2027 intake. I am currently finishing a B.S. in Environmental Science at Western State University, where I have been working in Dr. Priya Raman's hydrology lab on a project modeling groundwater recharge in the eastern basin. I have read your recent paper on aquifer depletion and was particularly interested in your approach to integrating remote sensing with local well data. I would be glad to share my lab work or discuss your research further if you have time this spring. Thank you for your consideration. Sincerely, Jordan Ortiz.",
            "Municipal composting programs are one of the cheapest climate interventions available to a mid-sized city, and most of them pay for themselves within a decade. Food waste accounts for roughly a quarter of what goes into American landfills, where it decomposes without oxygen and releases methane, a gas more than twenty-five times more potent than carbon dioxide over a twenty-year window. A curbside composting program diverts that waste into soil amendment instead. The upfront costs are real — collection trucks, processing facilities, resident education — but they are one-time costs against a permanent reduction in emissions. Cities that have done it report diversion rates above forty percent within five years.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # 3 human, 3 ai, 3 borderline to cover the range of scores
        # Provenance:
        # 1 Personnal narrative / reflective	NYT Tiny Memoir Contest winners
        # 2	Casual, typo-heavy	Reddit comment thread
        # 3	Academic literary	Mark Twain, Life on the Mississippi, “Reading the River”
        "texts": [
            "I fidgeted in the car, adjusting my SWAT gear. We parked, ready for a sugar raid. Dad shut the car door too soon. Bam! Part of my finger went with it. The back seat turned into triage. Mom tore off her Viking beard, wrapping it tight around my finger. My sisters cried as if they lost their fingers. Dad searched the car for my fingertip, nothing. Relief settled in on the way back from the E.R. It would heal, the doctor said. Two years later, the car has new owners. If they find what we failed to … well, happy Halloween.",
            "My high school had 4 guidance counselors. 3 were competent at their jobs. Mine opened the top draw of his desk and had a rotisserie chicken in it which he then proceeded to eat while attempting to explain why choosing a college is important. I'm not sure what I took away from that experience. Always expect a rotisserie chicken, I guess. At least he put the food under his own hat, rather than someone else's, UNLIKE Poodley P. McFustercluck: I remember a time when an honest dawg could bring in an entire rotisserie chicken to the theater without needing to hide it under his comically oversized cowboy hat. WE USED TO BE A COUNTRY!!! we used to wear parachute pants.",
            "It turned out to be true. The face of the water, in time, became a wonderful book—a book that was a dead language to the uneducated passenger, but which told its mind to me without reserve, delivering its most cherished secrets as clearly as if it uttered them with a voice. And it was not a book to be read once and thrown aside, for it had a new story to tell every day. Throughout Chapter 3 the long twelve hundred miles there was never a page that was void of interest, never one that you could leave unread without loss, never one that you would want to skip.",
            # AI generated samples by deepseek free tier
            "When I was twelve I broke my wrist trying to prove I could jump a fence in one motion. I remember the sound more than the pain — a clean snap that seemed to come from somewhere outside my body. My friend Ben ran to get his mother while I sat in the grass staring at my arm, which had developed a second elbow. The emergency room took four hours. The doctor asked how it happened, and I said skateboarding, because it sounded less stupid than the truth. My mother didn't correct me. She just looked at me the way she did when she was deciding whether to laugh.",
            "Genuinely cannot believe my school decided the best time to renovate the library was the three weeks before finals. There's a jackhammer going from 7am. 7am. I have a paper due Friday and my options are: study in the hall where a guy is screaming into his phone about a group project, or study in the cafeteria where they're playing the same five songs on a loop. I tried the library anyway and a guy in a hard hat told me I couldn't be there, which like, fair, but also it's literally called the library. Anyway I'm writing this from my car. It's 88 degrees. I have four more hours of this.",
            "In The Yellow Wallpaper, Gilman never lets the narrator name her own condition, which is precisely the point. She describes the wallpaper in obsessive detail — the pattern that plunges off at a wild angle, the woman creeping behind it — while the vocabulary that would explain her situation is withheld. What struck me on a second reading is how the story's horror is structural rather than emotional. The prose stays calm, almost domestic, even as the narrator's world narrows to a single room. Gilman's achievement is that the reader notices the walls closing before the narrator does, and that discomfort becomes part of the story's argument.",
            # AI generated, human edits
            'Frost\'s "The Road Not Taken" is usually read as a poem about choice, but it\'s is more about how we narrate choice after the fact. The speaker admits the two roads were worn "really about the same," yet by the end he is certain he took the one less traveled. The irony of the poem is that this certainty is manufactured. The famous final line isn\'t wisdom, it is self congratulations.',
            "I started running last year mostly because I couldn't sleep. It wasn't about fitness or a race or any of the reasons people give when they talk about running. I just needed something to do between three and five in the morning, when I was already awake, but the rest of the world wasn't. The first few weeks were miserable and I nearly quit. Then something shifted. Now I notice things on the route I never saw before, like the bakery that starts proofing at four and the guy who walks his very old dog in the dark. Running didn't fix my sleep. It gave me somewhere to be while I waited for it to fix itself.",
            "Remote work has become a proxy for an argument about trust, and that is why the debate continues. Employers who demand a return to the office are rarely making a real estate decision; they are making a claim about supervision. Employees who resist are rarely making a commute decision; they are making a claim about autonomy. Both sides have evidence, but neither side's evidence addresses the other's actual concern. The practical result is a stalemate that erodes good will on both sides. A more effective conversation should perhaps be less about where work happens, and instead whether it is being done well.",
        ],
    },
    {
        "name": "appeal path",
        "criterion": 5,
        # 5 empty texts, appeals to be handled manually
        "bodies": [
            {"text": "word" * 80, "creator_id": "ai_for_appeal"},
            {"text": "word" * 80, "creator_id": "ai_for_appeal"},
            {"text": "word" * 80, "creator_id": "ai_for_appeal"},
            {"text": "word" * 80, "creator_id": "ai_for_appeal"},
            {"text": "word" * 80, "creator_id": "ai_for_appeal"},
        ],
    },
    {
        "name": "empty text",
        "criterion": 5,
        # 5 empty texts
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "", "creator_id": "eval_bad_empty"},
        ],
    },
    # A bad-input criterion looks like this. Uncomment and adjust if that's one
    # of your five — these are raw request bodies, sent exactly as written.
    #
    # {
    #     "name": "bad input",
    #     "criterion": 3,
    #     "bodies": [
    #         {"text": "", "creator_id": "eval_bad_empty"},
    #         {"creator_id": "eval_bad_missing"},          # no text field at all
    #         {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
    #         {"text": None, "creator_id": "eval_bad_null"},
    #     ],
    # },
    # TODO: add what your remaining criteria need.
    #
    # A criterion about the appeal path can't be tested by sending text alone;
    # it needs a submission first and then an appeal against the content_id
    # that came back. You'll need to test that one by hand, or extend this file
    # and run_eval.py to do it. Saying which you did is part of the write-up.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
