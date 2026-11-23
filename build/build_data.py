import os
"""Build site/data.json from _out/table.json (assembled from content/) plus the editorial spine (overview), Guide and exchanges (cluster views)."""
import json, re
D = json.load(open("_out/table.json"))
R = {r["id"]: r for r in D["rows"]}

SHORT = {'3.06': 'The standard reply', '1.06': 'Other minds (polite convention)', '1.17': 'Winograd Schema Challenge', '1.07': 'Various disabilities', '1.08': 'Lovelace objection', '1.14': 'Turing Test as thought experiment', '1.09': 'Continuity in the nervous system', '1.10': 'Informality of behavior', '1.11': 'Extrasensory perception', '2.08': 'Syntax is not semantics', '2.10': 'Original vs. derived content', '2.06': 'Intuition-pump objection', '6.05': 'Searle against Dennett', '3.02': 'Penrose: Gödel and quantum mind', '3.04': 'Intractability of learning', '7.10': 'Limits of transformers', '4.02': 'Dreyfus’s critique', '4.07': 'Autopoiesis and life–mind', '4.03': 'Heideggerian critiques', '5.01': 'Multiple realizability', '6.10': 'Could an LLM be conscious?', '6.06': 'Illusionism', '7.01': 'Distributional semantics', '7.06': 'Scaling and the bitter lesson', '7.05': 'Formal vs. functional competence', '7.13': 'Mechanistic interpretability', '8.01': 'Normative accounts of agency', '8.02': 'Autonomy as self-constitution', '8.06': 'Agency in LLM-based agents', '9.06': 'Full rights dilemma', '9.02': 'Personhood and rational agency', '9.08': 'Robots should be slaves', '9.03': 'Social-relational status', '10.01': 'Weizenbaum on computer reason', '10.03': 'AI as ideology', '10.08': 'Critique of anthropocentrism', '10.09': 'Indigenous kinship and Ubuntu', '11.07': 'Deceptive alignment', '2.14': 'Wittgenstein on “machines think”', '4.05': 'Fuchs: no living partner', '11.04': 'Orthogonality vs. risk argument', '5.08': 'Computationalism', '5.10': 'Systematicity challenge', '10.12': 'Hype as distraction', '10.13': 'Hidden costs', '6.12': 'Heterophenomenology', '5.11': 'The harder problem (Block)', '7.17': 'Cultural and social technologies', '7.18': 'LLMs understand us', '8.07': 'Minimal agency in RL systems', '9.12': 'Moratorium on synthetic minds', '9.13': 'Digital minds (Shulman & Bostrom)', '9.14': 'Self-reports as evidence', '10.14': 'The whiteness of AI', '11.10': 'Power-seeking AI (Carlsmith)'}
def short(a, rid=None):
    if rid in SHORT: return SHORT[rid]
    a = re.sub(r"\s*\([^)]*\)", "", a).strip()
    return a if len(a) <= 34 else a[:33].rsplit(" ", 1)[0] + "…"

# ---------------- overview: the questions in order ----------------
SPINE = [
 dict(key="Q0", q="Who asks, and why?",
      lede="Before asking whether machines think, ask who is asking, and why. Whose interests does the question serve? What does it distract us from? What should never be handed to machines? Who counts as a person?",
      lanes=[dict(label="Whose interests and knowledge does the question serve, and what does it hide?", ids=["10.12", "10.13", "10.03", "10.04", "10.05", "10.06", "10.14", "10.01"]),
             dict(label="Who counts as a person, and in which traditions?", ids=["10.07", "10.08", "10.09", "10.10", "10.11"])],
      next="With that in view, the first question is whether there is anything to find out."),
 dict(key="Q1", q="Is there a fact of the matter?",
      lede="Is it a fact about a system whether it thinks, understands or matters morally? Or is that something we confer, by how we treat it?",
      lanes=[dict(label="Yes, it is a fact about the system", note="Most arguments on both sides assume this. Searle and Chalmers doubt that machines have it; functionalists think they could.", ids=["2.01", "6.04", "5.01", "5.04", "2.12", "6.09"]),
             dict(label="The question itself is in question", note="Turing called “Can machines think?” too meaningless to discuss, and replaced it with a test.", ids=["1.01", "1.14", "1.16", "2.14", "7.05", "6.06"]),
             dict(label="It depends, partly or wholly, on how we treat it", note="Dennett (2.11) takes a middle view: the patterns are real, but which stance fits them is partly a practical matter. The others put the answer in relationships and practice.", ids=["2.11", "7.14", "9.03", "10.08"])],
      next="If it is a fact, what would make it true? Each rung of the ladder below is one answer. If it depends on how we treat it, the later questions become questions about practice: who is recognized, and on what terms (Q0 and Q4)."),
 dict(key="Q2", q="What would it take, and can computation supply it?",
      lede="A ladder of proposed conditions, roughly from thinner to thicker. Most rungs answer a counterexample to the one before; two come from separate traditions, and some arguments skip a rung or go back. The Guide’s section “Reading the Q2 ladder” sets this out. First comes a gate: can computation reach any rung at all? Chip colours show each argument’s stance on its cluster’s question, not whether it agrees with the column it sits in.",
      gate=dict(label="The gate: can computation get onto the ladder?", no=["1.04", "3.01", "3.02"], practice=["3.04", "3.05", "1.10", "7.10"], yes=["3.03"],
                note="Two kinds of limit. Formal limits say computation cannot, in principle, do what a mind does. Practical limits grant that machine thought is possible, and ask whether it is feasible.", reply="The standard reply: these limits apply to human minds too.", reply_id="3.06"),
      rungs=[
        dict(label="Behavior", why="Turing: if it plays the imitation game as well as we do, what else could we ask? Harnad raises the bar to all our capacities.", pro=["1.01", "1.06", "1.13"], yes=[], no=["1.12", "1.15", "1.05", "1.07", "1.08"], c=["1"],
             jumps=[dict(to=4, text="Harnad (1.13) asks for robotic as well as verbal capacities, which ground symbols in the world."), dict(to=7, text="Jefferson (1.05) asks for feeling, not just behavior.")]),
        dict(label="Running the right program", why="Strong AI, in Searle’s term: the right program is a mind, and behavior is only evidence of it.", pro=["5.08", "5.10", "2.02", "2.03"], yes=[], no=["2.01", "2.08", "2.09", "2.07"], c=["2"],
             step="Blockhead and the ELIZA effect: matching behavior is not enough, so look at the program that produces it."),
        dict(label="Functional organization", why="Functionalism: what matters is how the system is organized, not what it is made of.", pro=["5.01", "5.09", "2.05", "5.04"], yes=[], no=["5.02", "5.03", "5.07"], c=["2", "5"],
             step="The Chinese Room says a program is not enough; the brain simulator reply and functionalism answer that what matters is the causal organization that runs it, whatever it is made of.",
             jumps=[dict(to=6, text="IIT (5.06) goes from organization straight to physical structure, skipping life: non-living neuromorphic hardware could qualify.")]),
        dict(label="Grounding in the world", why="Symbols must be connected to what they are about.", pro=["2.13"], yes=["2.04", "2.12", "7.01", "7.18"], no=["2.10", "7.02", "7.03"], c=["2", "7"],
             step="The robot reply and the grounding problem: even the right organization needs its symbols connected to what they are about."),
        dict(label="Embodiment and life", why="Intelligence needs a body in the world, and perhaps a living one for which things matter.", pro=["4.01", "4.02", "4.07"], yes=["4.04", "4.06", "4.08"], no=["4.05", "4.09"], c=["4"],
             step="Dreyfus and the enactivists: connection to the world is not enough without a body that acts in it, and perhaps a life that is at stake.",
             jumps=[dict(to=3, text="Enactive AI (4.08) treats life as a kind of organization that could be built.")]),
        dict(label="The right substrate", why="What the system is made of matters, not just the software it runs.", pro=["5.05", "5.06", "1.09"], yes=["5.04"], no=[], c=["5"],
             step="A separate tradition. Even a self-maintaining artificial system might not be enough: on these views, what the system is made of matters, not just how it is organized."),
        dict(label="Felt experience", why="Even the right physical system seems to leave experience unexplained.", pro=["1.05", "6.01", "6.02", "6.03", "6.04"], yes=["5.04", "6.06", "6.07", "6.08"], no=["4.09", "5.05"], c=["6"],
             step="A separate tradition (Nagel, Jackson, Chalmers): even the right physical system seems to leave felt experience unexplained.",
             jumps=[dict(to=3, text="Fading qualia (5.04) argues that organization fixes experience, which brings this rung back to rung 3."), dict(to=3, text="Illusionism (6.06) explains the sense of experience by a self-model, again a matter of organization.")]),
      ],
      pro_label="Proposes this condition", yes_label="Says machines can meet it", no_label="Says it is not enough, or machines lack it",
      next="The thinner the condition you accept, the easier it is to test. Behavior is visible, organization partly, experience hardly at all."),
 dict(key="Q3", q="How could we tell?",
      lede="Whatever the answer to Q2, we need evidence. The methods differ in what they look at and how easily they are fooled.",
      lanes=[dict(label="Watch what it does", ids=["1.01", "1.13", "1.17", "7.08", "7.09"]),
             dict(label="Extrapolate from scale", note="Claims about what more scale will bring, not tests for a mind. Both are disputed.", ids=["7.06", "7.07"]),
             dict(label="Behavior can mislead", ids=["1.12", "1.15", "1.18", "6.11", "7.11", "10.02", "5.11"]),
             dict(label="Look inside", ids=["7.10", "7.12", "7.13"]),
             dict(label="Apply theories of consciousness", ids=["6.07", "6.08", "6.09", "6.10"]),
             dict(label="Ask what kind of thing it is", ids=["7.04", "7.05", "7.14", "7.17"]),
             dict(label="Ask whether it is saying anything", ids=["7.15", "7.16"]),
             dict(label="Take its words and actions as evidence, as with other minds", ids=["1.06", "6.12", "9.04", "9.14"])],
      next="Because the evidence stays uncertain, the last questions are answered under uncertainty: assign responsibility in advance, take precautions about welfare, manage risk."),
 dict(key="Q4", q="What follows?",
      lede="Some of these questions arise whether or not machines think: responsibility, misuse, our relationships with machines. Others depend on the earlier answers: what is owed to a machine depends on whether it can feel, and the case for catastrophic risk assumes that it pursues goals.",
      lanes=[dict(label="Can it act, and who is responsible?", ids=["8.01", "8.02", "8.03", "8.04", "8.05", "8.06", "8.07", "4.10"]),
             dict(label="Is anything owed to it?", ids=["9.01", "9.02", "9.04", "9.05", "9.06", "9.07", "9.08", "9.09", "9.10", "9.11", "9.12", "9.13"]),
             dict(label="Could it harm us?", ids=["11.01", "11.02", "11.03", "11.04", "11.05", "11.06", "11.07", "11.08", "11.09", "11.10"])],
      next=None),
]

# ---------------- exchanges (clusters 1 and 2 first) ----------------
X = {
 "1": [
  dict(title="Turing’s proposal and his nine objections",
       claim="If a machine can play the imitation game as well as a person, we should say that it thinks.",
       moves=[
        dict(key="t1", side="A", type="Proposal", id="1.01", gist="Replace “Can machines think?” with a question we can test: can it pass for a person in conversation?", to="claim"),
        dict(key="obj", side="D", type="Objections", title="Turing’s nine objections, sorted by how he answers them", to="claim", groups=[
          dict(label="Set aside", items=[
            dict(id="1.02", reply="limits God’s omnipotence; theology has misjudged science before"),
            dict(id="1.03", reply="a consolation, not an argument")]),
          dict(label="Answered", items=[
            dict(id="1.07", reply="unsupported inductions from the machines we know; often the consciousness objection in disguise"),
            dict(id="1.08", reply="machines surprise us; learning machines go beyond their orders"),
            dict(id="1.09", reply="a discrete machine can imitate a continuous one closely enough"),
            dict(id="1.11", reply="taken seriously: use a telepathy-proof room")]),
          dict(label="Answered, but carried on elsewhere", items=[
            dict(id="1.04", reply="humans have limits too", pass_=["3.01"]),
            dict(id="1.05", reply="we grant other people minds on the same evidence (see 1.06)", pass_=["6.04"]),
            dict(id="1.10", reply="rules of conduct are not laws of behavior", pass_=["3.05", "4.02"])])]),
        dict(key="t2", side="A", type="Reply", id="1.06", gist="We have no deeper access to other people. Consistency requires the same courtesy for a machine that behaves as they do.", to="obj:1.05"),
       ],
       stands="Turing’s replies dispose of several objections, but three were passed on rather than settled. The consciousness objection became the hard problem, the mathematical objection the Gödelian arguments, and the informality objection the frame problem and Dreyfus’s critique.",
       passes=[dict(id="6.04", why="Jefferson’s objection, developed"), dict(id="3.01", why="the mathematical objection, developed"),
               dict(id="3.05", why="informality becomes the frame problem"), dict(id="4.02", why="and Dreyfus’s critique")]),
  dict(title="Is behavior enough?",
       claim="Behavior that matches a thinker’s is enough to show thought.",
       moves=[
        dict(key="b1", side="D", type="Counterexample", id="1.12", gist="A vast lookup table could pass a time-limited test with no intelligence at all. How behavior is produced matters.", to="claim"),
        dict(key="b2", side="A", type="Raise the bar", id="1.13", gist="Concede that verbal behavior is not enough; demand indistinguishability across all our capacities, robotic as well as verbal.", to="claim"),
        dict(key="b3", side="M", type="Reframe", id="1.14", gist="Gonçalves: the imitation game is a thought experiment, not a benchmark. Turing varied it to answer his opponents and to suggest a hypothesis about learning machines.", to="claim"),
        dict(key="b4", side="D", type="Case", id="1.15", gist="People attribute understanding to a simple pattern-matcher. Conversational competence is cheap.", to="claim"),
        dict(key="b5", side="A", type="Better test", id="1.17", gist="Commonsense pronoun puzzles should be hard to pass by tricks.", to="b4"),
        dict(key="b6", side="D", type="Case", id="1.18", gist="High scores can come from shortcuts that do not transfer, as with Clever Hans.", to="b5"),
        dict(key="b7", side="A", type="Diagnosis", id="1.16", gist="Each time a test is passed, critics may redefine intelligence. If so, the denial is unfalsifiable, which takes away the skeptic’s reason for saying that behavior is not enough.", to="claim"),
       ],
       stands="Behavior is now treated as evidence whose weight depends on how hard it is to fake, not as proof either way. The fight moves to how we could tell.",
       passes=[dict(id="2.01", why="a related counterexample, aimed at the right program rather than the right behavior"), dict(id="6.11", why="faking the markers of consciousness"),
               dict(id="7.11", why="shortcuts in LLM reasoning")]),
 ],
 "2": [
  dict(title="The Chinese Room and the replies",
       claim="Running the right program is enough for understanding (what Searle calls strong AI).",
       moves=[
        dict(key="m1", side="D", type="Counterexample", id="2.01", gist="Searle follows the program for Chinese by hand. Fluent answers come out; he understands none of it.", to="claim"),
        dict(key="m2", side="A", type="Redescription", id="2.02", gist="Searle in the room is one part of a system. The whole system understands.", to="m1"),
        dict(key="m3", side="D", type="Rejoinder", label="Searle’s rejoinder (in 2.01)", gist="Let him memorize the rules and work outdoors. He is now the whole system, and still understands nothing.", to="m2"),
        dict(key="m4", side="A", type="Refinement", id="2.03", gist="The program creates a virtual mind distinct from the man. Memorizing the rules does not touch it.", to="m3"),
        dict(key="m5", side="A", type="Added condition", id="2.04", gist="Concede the room, but connect the program to cameras and motors.", to="m1"),
        dict(key="m6", side="D", type="Rejoinder", label="Searle’s rejoinder (in 2.01)", gist="Camera inputs reach the man as more symbols. Nothing changes.", to="m5"),
        dict(key="m7", side="A", type="Different program", id="2.05", gist="Simulate a Chinese speaker’s brain, neuron by neuron.", to="m1"),
        dict(key="m8", side="D", type="Rejoinder", label="Searle’s rejoinder (in 2.01)", gist="A man operating water pipes that simulate the neurons still understands nothing; the simulation copies only the formal structure.", to="m7"),
        dict(key="m8b", side="D", type="Generalization", id="2.07", gist="A simulated storm makes nobody wet. Simulating a brain is not duplicating its causal powers.", to="m8"),
        dict(key="m9", side="M", type="Method challenge", id="2.06", gist="We picture a slow, simple rule-follower. That intuition is unreliable for a system fast and complex enough to pass.", to="m1"),
        dict(key="m10", side="D", type="Formalization", id="2.08", gist="Programs are syntax, minds have semantics, and syntax is not sufficient for semantics.", to="claim"),
        dict(key="m11", side="D", type="Generalization", id="2.09", gist="Nothing is a computer intrinsically; computation is relative to an observer.", to="m10"),
       ],
       stands="There is no agreed verdict on which reply works. The fight moves from programs to meaning: what would connect a system’s symbols to the world?",
       passes=[dict(id="5.03", why="an earlier, parallel move against functionalism"), dict(id="5.05", why="Searle’s positive view"),
               dict(id="7.02", why="the room updated for LLMs"), dict(id="1.12", why="a related counterexample, aimed at behavior rather than programs")]),
  dict(title="What fixes meaning?",
       claim="A machine’s symbols could mean something to the machine itself, not only to us.",
       moves=[
        dict(key="n1", side="D", type="Distinction", id="2.10", gist="Artifacts’ meanings are derived from ours. Only minds have original intentionality.", to="claim"),
        dict(key="n2", side="M", type="Dissolution", id="2.11", gist="There is no further fact. Having beliefs is being well predicted by the intentional stance.", to="n1"),
        dict(key="n3", side="D", type="Problem", id="2.13", gist="Meanings in a pure symbol system are parasitic on ours, like a Chinese–Chinese dictionary. Only symbols grounded in sensorimotor categories, which a robot could have, mean something to the system.", to="claim"),
        dict(key="n4", side="A", type="Naturalization", id="2.12", gist="Causal and historical relations to the world fix content, and a machine could stand in them.", to="n1"),
        dict(key="n5", side="M", type="Conceptual remark", id="2.14", gist="“A machine cannot think” is not an empirical claim: we say “thinks” of human beings and what resembles them, so the question concerns our concepts.", to="claim"),
       ],
       stands="Grounding is the question that language models revived: can text alone ground meaning? Naturalized semantics and the intentional stance offer different routes to yes.",
       passes=[dict(id="7.02", why="the octopus test"), dict(id="7.01", why="meaning from patterns of use"),
               dict(id="1.13", why="Harnad’s robotic test"), dict(id="9.03", why="the relational route, for moral status")]),
 ],
}
exec(open('build/ex_3_11.py').read()); X.update(X2)

# ---------------- AI on AI (Claude's assessment), from the workbook tab ----------------
PICKS = {"1": (["1.12", "1.18", "1.06", "1.16"], ["1.02", "1.03", "1.11", "1.07"]),
         "2": (["2.13", "2.02", "2.11"], ["2.08", "2.09"]),
         "3": (["3.04", "3.05"], ["3.01", "3.02"]),
         "4": (["4.07", "4.09", "4.02"], ["4.06", "4.05"]),
         "5": (["5.04", "5.07"], ["5.03"]),
         "6": (["6.11", "6.09"], []),
         "7": (["7.11", "7.10", "7.12", "7.13", "7.05"], ["7.03", "7.08"]),
         "8": (["8.04", "8.02"], ["8.03"]),
         "9": (["9.07", "9.09", "9.08"], ["9.04"]),
         "10": (["10.02", "10.03", "10.01"], ["10.04"]),
         "11": (["11.06", "11.05", "11.04"], ["11.01"]),
         "all": (["1.12", "1.18", "6.11", "4.07", "4.09", "2.13", "8.04", "11.06", "10.03"], [])}
AION = []
for row in D["ai_on_ai"][1:]:
    k = "all" if row[0].startswith("Overall") else row[0].split(".")[0]
    s, w = PICKS[k]
    assert all(i in R for i in s + w)
    AION.append(dict(k=k, q=row[1], strong_txt=row[2], weak_txt=row[3], land=row[4], follow=row[5], strong=s, weak=w))
AION_INTRO = D["ai_on_ai_intro"][1]
import glob
MODELS = [] if os.path.exists("content/ai_models/claude.json") else [dict(key="claude", name="Claude", maker="Anthropic", collected="19 November 2026", collected_by="Daniel Estrada",
               method="Written by Claude while building the Atlas, with the whole table in view. Claude made the map, so its picks also shaped how the arguments are presented.",
               intro=AION_INTRO, rows=AION)]
for p in sorted(glob.glob("content/ai_models/*.json")):
    m = json.load(open(p))
    for row in m["rows"]:
        assert row["k"] in PICKS, (p, row["k"])
        for i in row["strong"] + row["weak"]:
            assert i in R, (p, i)
    MODELS.append(m)
MODELS.sort(key=lambda m: m["name"].lower())   # alphabetical: no model is listed first by default
BLIND = os.environ.get("BLIND") == "1"
if BLIND:   # review copy: no model's entries, an empty template in their place
    CL = {c["key"]: c["name"] for c in D["clusters"]}
    MODELS = [dict(key="template", name="[Model name]", maker="—", collected="—", collected_by="",
                   method="This copy of the Atlas has no AI model’s entries. The rows below are the empty template each model fills in.",
                   intro="[A short note, in the first person: who you are, and how far your judgments may reflect your training and your maker.]",
                   rows=[dict(k=k, q="[The question this cluster asks, for systems like you]", strong=[], weak=[],
                              strong_note="[The arguments you find strongest, by ID]", weak_note="[The arguments you find least convincing, by ID]",
                              land="[Where you land]", follow="[What follows if the strongest arguments go through]",
                              strong_txt="[Why these are strongest]", weak_txt="[Why these are least convincing]") for k in list(CL) + ["all"]])]
    AION = []
    AION_INTRO = ""   # nothing from any model's entry in the review copy


GUIDE_LADDER = dict(
 intro="The ladder lists conditions that have been proposed for a machine to think, roughly from the thinnest (behavior) to the thickest (felt experience). It is an interpretation, not a settled hierarchy. Most rungs were proposed in reply to a counterexample to the rung before, so reading along the ladder retraces part of the debate’s history. Two rungs come from separate traditions, and some arguments skip rungs or go back.",
 steps=[
  ["From behavior to the right program", "Turing proposed that a machine that plays the imitation game as well as we do should be said to think (1.01). Block’s Blockhead (1.12) imagines a machine that passes a time-limited test by looking up stored replies, with no intelligence at all, and the ELIZA effect (1.15) shows how easily people credit a simple program with understanding. If the right behavior can come from a mindless process, what matters is how it is produced: the program. That is the position Searle called strong AI."],
  ["From the program to functional organization", "Searle’s Chinese Room (2.01) targets strong AI: a person can run the program for Chinese by hand without understanding Chinese, so running a program is not enough. The best-known replies say that the person is only one part of the system (2.02), or that a program simulating a Chinese speaker’s brain, neuron by neuron, would understand (2.05). Both move the condition from the program as written to the organization of the whole running system, whatever it is made of: functionalism (5.01)."],
  ["From organization to grounding in the world", "The robot reply (2.04) grants that a system sealed off from the world might not understand, and connects the program to cameras and motors. Harnad’s symbol grounding problem (2.13) sharpens the point: a system’s symbols mean something only if they are connected to the things they are about, not just to other symbols. Language models raise the question again, since they learn from text alone (7.01, 7.02, 7.03)."],
  ["From grounding to a body and a life", "Dreyfus (4.02) and the phenomenologists argue that a connection to the world is not enough. Human intelligence is skilled bodily coping in a situation, not the manipulation of representations. Enactivists (4.07) go further: a mind belongs to a living system that maintains itself and for which things matter. Defenders of embodied and enactive AI (4.04, 4.06, 4.08) reply that artificial systems could meet these conditions."],
  ["From life to the right substrate", "This rung comes from a different tradition. Searle’s biological naturalism (5.05) and integrated information theory (5.06) hold that what a system is made of, or its physical cause-and-effect structure, matters, not just how it is organized. It is the more demanding claim: even a self-maintaining artificial system might be made of the wrong stuff."],
  ["From substrate to felt experience", "The top rung comes from the philosophy of consciousness. Nagel (6.01), Jackson (6.03) and Chalmers (6.02, 6.04) argue that even a complete physical account seems to leave felt experience unexplained. If thinking requires experience, no lower rung guarantees it, and it is not clear how anyone could tell (Q3)."],
 ],
 jumps_title="Where the ladder is not one scale",
 jumps_intro="Some arguments do not climb one rung at a time.",
 jumps=["Harnad’s Total Turing Test (1.13) keeps behavior as the test but asks for robotic as well as verbal abilities, the abilities that would ground symbols. It jumps from rung 1 to rung 4.",
        "Jefferson’s objection (1.05) jumps from behavior straight to felt experience: a machine would have to feel, not just respond.",
        "Integrated information theory (5.06) skips life: it requires the right physical cause-and-effect structure, which non-living neuromorphic hardware could have.",
        "Enactive AI (4.08) folds life back into organization: if life is a kind of self-maintaining organization, it could be built.",
        "Chalmers’s fading qualia argument (5.04) holds that experience follows functional organization, which would bring the top rung back down to rung 3. Illusionism (6.06) also explains the sense of having experience in terms of organization, as a self-model."],
 close="So the ladder is best read as one path through the debate, which shows how each condition was proposed, not as a scale that every view accepts.")

GUIDE = dict(
 intro="How to read the Atlas: what its marks mean and the terms it uses. The questions, placements, exchanges and families are interpretations, and the summaries are paraphrases, not quotations.",
 senses=[["Intelligence", "solving problems and reaching goals across many situations"], ["Linguistic competence", "producing and responding to language fluently"],
         ["Understanding", "grasping what words, situations or problems mean"], ["Intentionality", "having states that are about things, with content"],
         ["Consciousness", "there being something it is like to be the system; felt experience"], ["Self-awareness", "representing oneself as oneself"],
         ["Agency and autonomy", "acting on one’s own goals, and perhaps setting them"], ["Moral agency", "being answerable for what one does"],
         ["Sentience and moral status", "being able to fare well or badly, so that one’s interests count"]],
 senses_note="A system might have some of these and not others. Passing a behavioral test does not settle consciousness or moral status, and doubts about consciousness do not show that a system lacks cognitive abilities. Each argument’s panel names its target.",
 marks=[["Stance", "Green: for the possibility in the cluster’s question (that machines can think, understand, be conscious, act as agents or have moral status; in cluster 11, that AI poses serious risk). Red: against it. Grey: reframes or dissolves the question."],
        ["Chips", "Each chip is one argument: its ID (which matches the workbook) and a short name, with its stance on the left edge. Click it for the summary, source and links."],
        ["Ladder", "In Q2, each tile is a proposed condition, roughly from thinner to thicker. “Reading the Q2 ladder”, below, explains what moved the debate from one condition to the next."], ["Checked summaries", "Every summary has been checked against an abstract, an encyclopedia entry or an open copy of the source. That is not a specialist’s review, so read the source before relying on a summary."], ["Deflationary", "Grey is a second-order stance, not a shared doctrine: it covers views that dissolve the question, views that make it a matter of degree, and views that reject the property-first framing."], ["Exchanges", "Each cluster view shows exchanges. A contested claim sits at the top. Moves that affirm it are on the left, moves that reframe it in the middle, moves that deny it on the right. Numbers give the order, and arrows show what each move answers; hover over a move to trace its arrows."],
        ["Hand-offs", "Coloured tags under “Where the argument goes next” lead to arguments in other clusters, in that cluster’s colour."],
        ["Families", "Families group arguments that make the same kind of move in different clusters. Highlight one below the overview."],
        ["AI on AI", "Ringed chips are a model’s strongest picks; faded, dashed chips its least convincing."]],
 terms=[["Behaviorism (about minds)", "the view that having a mind is a matter of behavior or dispositions to behave"],
        ["Functionalism", "the view that mental states are defined by their causal roles, so they could be realized in different materials"],
        ["Computationalism", "the view that thinking is computation over representations"],
        ["Connectionism", "modeling cognition with networks of simple units whose connection weights are learned"],
        ["Intentionality", "the aboutness of mental states: a belief is about something"],
        ["Original vs derived intentionality", "meaning a system has in its own right, as opposed to meaning we assign to it (as with words on a page)"],
        ["Symbol grounding", "how a system’s symbols come to be connected to what they stand for"],
        ["Qualia", "the felt qualities of experience, such as how red looks"],
        ["The hard problem", "why physical processing is accompanied by experience at all"],
        ["Illusionism", "the view that experience, as we usually describe it, is an introspective illusion"], ["Heterophenomenology", "Dennett’s method of treating a subject’s reports about experience as data to be explained, without assuming they are true or false (6.12)"],
        ["Enactivism", "the view that mind arises from a living organism’s activity in its world"],
        ["Autopoiesis", "self-production: a living system continually producing and maintaining itself"],
        ["Multiple realizability", "the same mental state being realized in different physical systems"],
        ["Moral patient", "a being to whom things can be owed; contrast moral agent, a being that can be answerable"],
        ["Alignment", "making an AI system pursue the goals its designers and users intend"],
        ["Orthogonality thesis", "the claim that intelligence and final goals can vary independently"],
        ["Instrumental convergence", "the claim that many final goals favor the same subgoals, such as acquiring resources"]],
 dates="Claims about current AI systems describe studies published up to 2025 and early 2026. This part of the map will date fastest; check for newer work before relying on it.",
 scope="This is a map of the debate about machine minds, not of AI ethics as a whole. Bias, surveillance, labor and environmental costs appear where they bear on how the question is framed and whose interests it serves (cluster 10).",
 ladder=GUIDE_LADDER, aion_note="Read the AI on AI page as a case study in how AI systems argue about systems like themselves, not as a verdict. The assessments are generated and unsourced. A model’s first-person statements are not evidence that it has the states it describes. Its picks may reflect its training and its maker’s interests, and models agreeing does not make them right. Criticize them as you would any participant in the debate.")
# checks
def ids_in(x):
    out = []
    for m in x["moves"]:
        if m.get("id"): out.append(m["id"])
        for g in m.get("groups", []):
            out += [i["id"] for i in g["items"]]
    return out
for k, exs in X.items():
    cov = [i for x in exs for i in ids_in(x)]
    allc = sorted(r["id"] for r in D["rows"] if r["cluster"] == k)
    assert sorted(set(cov)) == allc, (k, set(allc) - set(cov))
    for x in exs:
        for p in x["passes"]: assert p["id"] in R
for s in SPINE:
    for l in s.get("lanes", []): assert all(i in R for i in l["ids"]), l
    for r in s.get("rungs", []): assert all(i in R for i in r["pro"] + r["yes"] + r["no"]), r

out = dict(
 clusters=[dict(k=c["key"], tab=c["tab"], name=c["name"], q=c.get("question", "")) for c in D["clusters"]],
 rows=[dict(id=r["id"], c=r["cluster"], g=r["thread"], o=r.get("order", 99), s=r["stance"], a=r["arg"], sh=short(r["arg"], r["id"]), t=r["target"], sc=r["scope"],
            sum=r["summary"], orig=r["orig"], link=r["link"], f=r["family"], chk=0 if r["ver_status"][1].startswith("Paraphrase") else 1) for r in D["rows"]],
 rel=[dict(a=r[0], r=r[2], b=r[3], n=r[5]) for r in D["relations"][1:]],
 fam=D["family_defs"], kernel=D["kernel_defs"], spine=SPINE, ex=X, aion=AION, aion_intro=AION_INTRO, models=MODELS, guide=GUIDE)
s = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
open("_out/data_blind.json" if BLIND else "site/data.json", "w").write(s)
print("data.json", len(s), "bytes")
