from enum import Enum, unique


@unique
class Questions(Enum):

    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
    _10 = 10
    _11 = 11
    _12 = 12
    _13 = 13
    _14 = 14
    _15 = 15
    _16 = 16
    _17 = 17
    _18 = 18
    _19 = 19
    _20 = 20
    _21 = 21
    _22 = 22
    _23 = 23
    _24 = 24
    _25 = 25
    _26 = 26
    _27 = 27
    _28 = 28
    _29 = 29
    _30 = 30
    _31 = 31
    _32 = 32
    _33 = 33
    _34 = 34
    _35 = 35
    _36 = 36
    _37 = 37
    _38 = 38
    _39 = 39
    _40 = 40
    _41 = 41
    _42 = 42
    _43 = 43
    _44 = 44
    _45 = 45

QUESTION_CHOICES = (
    (Questions._1.value, "Have you ever donated blood, plasma or blood cells in the past?"),
    (Questions._2.value, "Have you ever been excluded from blood donation as ineligible?"),
    (Questions._3.value, "Are you in good health?"),
    (Questions._4.value, "Is your weight over 50 kg?"),
    (Questions._5.value,
     "Have you been treated by a dentist or dental hygienist in the past 72 hours ?"),
    (Questions._6.value,
     "Have you been using any medication in the past month? Which medication?"),
    (Questions._7.value, "Have you suffered from fever over 38°C, herpes, diarrhea, sucked in tick, animal bite in the past month?"),
    (Questions._8.value, "Have you been vaccinated in the past month?"),
    (Questions._9.value, "Have you ever suffered or are you currently suffering from infectious disease such as: tuberculosis, boreliosis, toxoplasmosis, brucellosis, infectious mononucleosis, listeriosis, tularemia, babesiosis, Q-fever?"),
    (Questions._10.value, "Have you ever suffered or are you currently suffering from tropical disease: malaria, leishmaniasis, Chagas disease (trypanosomiasis)?"),
    (Questions._11.value, "Have you ever suffered or are you currently suffering from rheumatic disorders, rheumatic fever or autoimmune disease?"),
    (Questions._12.value, "Have you ever suffered or are you currently suffering from heart disease, high or low blood pressure?"),
    (Questions._13.value, "Have you ever suffered or are you currently suffering from chronic lung or bronchi disease, asthma, allergy, hay fever/pollinosis?"),
    (Questions._14.value,
     "Have you ever suffered or are you currently suffering from kidney disease?"),
    (Questions._15.value, "Have you ever suffered or are you currently suffering from blood disease, bleeding/hemorrhage symptoms?"),
    (Questions._16.value, "Have you ever suffered or are you currently suffering from nervous system disease, epilepsy?"),
    (Questions._17.value, "Have you ever suffered or are you currently suffering from metabolism disorders (for ex. diabetes) or endocrine disease (for ex. thyroid gland disease)?"),
    (Questions._18.value, "Have you ever suffered or are you currently suffering from skin diseases (eczema, psoriasis)?"),
    (Questions._19.value, "Have you ever suffered or are you currently suffering from digestive system, liver or pancreas disease?"),
    (Questions._20.value,
     "Have you ever suffered or are you currently suffering from tumor disease?"),
    (Questions._22.value, "Have you ever suffered or are you currently suffering from sexually transmissible disease?"),
    (Questions._23.value, "Have you experienced an inexplicable weight loss, raised temperature, sweating, behavioral changes, enlarged lymphatic nods in the past twelve months?"),
    (Questions._24.value, "Have you been treated for acne by isotretinoine (RoaccutaneR, AccutaneR), for prostate by finasteride or dutasterid (ProscarR, AvodartR, DuodartR), and for baldness (PropeciaR) in the past three months?"),
    (Questions._25.value, "Have you been treated by acitretin (NeotigasonR) or etretinate (TegisonR ) in the past three years?"),
    (Questions._26.value, "In the past six months have you had any operation, medical examination or treatment, endoscopy , arterial catheterization?"),
    (Questions._27.value, "In the past six months have you had any tattooing, piercing, ear-ring application, acupuncture, permanent make – up ?"),
    (Questions._28.value, "In the past six months have you had any injury during which the wound or mucous membrane was in contact with another person’s blood, or any accidental stick of a used needle?"),
    (Questions._29.value,
     "Have you ever received a blood component transfusion? If yes, when?.where?"),
    (Questions._30.value, "Have you ever received human or animal tissue or organ transplant (e.g. corneal transplantation, dura mater graft….)?"),
    (Questions._31.value, "Have you ever undergone brain or spinal cord surgery ?"),
    (Questions._32.value, "Have you had any information about Creutzfeldt-Jacob disease or about another spongiform encephalopathy in your family?"),
    (Questions._33.value, "Have you ever been treated with a products prepared from hypophysis (e.g. growth hormone)?"),
    (Questions._34.value, "Did you spend the time in excess of six moths in the United Kingdom/Ireland during 1980–1996?"),
    (Questions._35.value, "Have you been out of Slovak Republic in the past six months?"),
    (Questions._36.value, "Were you born or have you ever lived more than 6 month out of Europe? If yes, where? Since when do you live in Europe?"),
    (Questions._37.value, "Have you been in contact with any person suffering from hepatitis or another infectious disease in the past six months, ?"),
    (Questions._38.value,
     "Have you had a sexual intercourse with new partner in the past three months?"),
    (Questions._39.value, "Have you or your sexual partner ever been in any of the following risk situations: positive test for the HIV or hepatitis (jaundice)?"),
    (Questions._40.value, "Have you or your sexual partner ever been in any of the following risk situations: use of drugs or anabolic hormones?"),
    (Questions._41.value, "Have you or your sexual partner ever been in any of the following risk situations: payment for sex or performing sex for money or drugs?"),
    (Questions._42.value, "Do you have a risky occupation/hobbies? (professional driver, diver, worker in the height)?"),
    (Questions._43.value, "Male Donors: Have you had a sexual intercourse with a man in the past twelve months?"),
    (Questions._44.value,
     "Female Donors: Have you been pregnant or breast feeding in the past six months?"),
    (Questions._45.value, "Female Donors: Have you been treated with hormonal injection for sterility before 1986 ?")
)
