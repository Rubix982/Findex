def custom_porter_algorithm(input_str: str):

    # PREPROCESSING
    input_str = input_str.lower()

    # VARIABLE SECTION
    '''
    USED IN STEP 1A
    '''
    from_str = ['sess', 'ies', 'ss', 's']
    to_str = ['ss', 'i', 'ss', '']

    '''
    USED IN STEP 1B
    '''
    vowel_list = ['a', 'e', 'i', 'o', 'u']

    '''
    USED IN STEP 2
    '''
    from_suffix_consideration = ['ational', 'tional', 'enci', 'izer', 'abli', 'alli', 'entli', 'ousli', 'ization',
                                 'ation', 'ator', 'alism', 'iveness', 'fulness', 'ousness', 'aliti', 'ivitti', 'biliti', 'anci', 'eli']
    to_suffix_consideration = ['ate', 'tion', 'ence', 'ize', 'able', 'al', 'ent', 'ous',
                               'ize', 'ate', 'ate', 'al', 'ive', 'ful', 'ous', 'al', 'ive', 'ble', 'ance', 'e']

    '''
    USED IN STEP 3
    '''
    from_ication_suffix = ['icate', 'ative',
                           'alize', 'iciti', 'ical', 'ful', 'ness']
    to_ication_suffix = ['ic', '', 'al', 'ic', 'ic', '', '']

    '''
    USED IN STEP 4
    '''
    from_one_plus_suffix_consider = ['al', 'ance', 'ence', 'er', 'ic', 'able', 'ible',
                                     'ant', 'ement', 'ment', 'ent', 'ion', 'ou', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize']

    # 1st STEP SECTION

    '''
    Step 1A

    1. SESS -> SS
    2. IES -> I
    3. SS -> SS
    4. S -> Remove
    '''

    zipped_list = zip(from_str, to_str)

    for item in zipped_list:
        if input_str.endswith(item[0]):
            input_str = input_str[0: len(input_str) - len(item[0])] + item[1]

    '''
    Step 1B

    1. (m > 0)EED -> EE
    2. *[V]ED -> *[V]
    3. *[V]ING -> *[V]
    '''
    if len(input_str) > 3:
        if input_str.endswith('eed'):
            input_str = input_str[0: len(input_str) - len('eed')] + 'ee'

        if input_str.endswith(('ed')) and input_str[-3] in vowel_list:
            input_str = input_str[0: len(input_str) - len('ed')] + ''

        if input_str.endswith(('ing')) and input_str[-3] in vowel_list:
            input_str = input_str[0: len(input_str) - len('ing')] + ''

    '''
    Step 1C

    1. *[V]Y -> *[V]i
    '''
    if len(input_str) > 2:
        if input_str.endswith('y') and input_str[-2] in vowel_list:
            input_str = input_str[0: len(input_str) - len('y')] + 'i'

    # 2nd STEP SECTION

    '''
    Step 2
     
    1. (m>0)ATIONAL -> ATE
    2. (m>0)TIONAL -> TION
    3. (m>0)ENCI -> ENCE
    4. (m>0)IZER -> IZE
    5. (m>0)ABLI -> ABLE
    6. (m>0)ALLI -> AL
    7. (m>0)ENTLI -> ENT
    8. (m>0)OUSLI -> OUS
    9. (m>0)IZATION -> IZE
    10. (m>0)ATION -> ATE
    11. (m>0)ATOR -> ATE
    12. (m>0)ALISM -> AL
    13. (m>0)IVENESS -> IVE
    14. (m>0)FULNESS -> FUL
    15. (m>0)OUSNESS -> OUS
    16. (m>0)ALITI -> AL
    17. (m>0)IVITI -> IVE
    18. (m>0)BILITI -> BLE
    19. (m>0)ANCI -> ANCE
    20. (m>0)ELI -> E
    '''

    zipped_suffix_list = zip(from_suffix_consideration,
                             to_suffix_consideration)

    for suffix in zipped_suffix_list:
        if len(input_str) > len(suffix[0]) + 1:
            if input_str.endswith(suffix[0]):
                input_str = input_str[0: len(
                    input_str) - len(suffix[0])] + suffix[1]

    # 3rd STEP SECTION

    '''
    Step 3

    1. (m>0)ICATE -> IC
    2. (m>0)ATIVE -> ''
    3. (m>0)ALIZE -> AL
    4. (m>0)ICITI -> IC
    5. (m>0)ICAL -> IC
    6. (m>0)FUL -> ''
    7. (m>0)NESS -> ''
    '''

    zipped_ication_suffix = zip(from_ication_suffix,
                                to_ication_suffix)

    for suffix in zipped_ication_suffix:
        if len(input_str) > len(suffix[0]) + 1:
            if input_str.endswith(suffix[0]):
                input_str = input_str[0: len(
                    input_str) - len(suffix[0])] + suffix[1]

    # 4th STEP SECTION

    '''
    Step 4

    1. (m>1)AL -> ''
    2. (m>1)ANCE -> ''
    3. (m>1)ENCE -> ''
    4. (m>1)ER -> ''
    5. (m>1)IC -> ''
    6. (m>1)ABLE -> ''
    7. (m>1)IBLE -> ''
    8. (m>1)ANT -> ''
    9. (m>1)EMENT -> ''
    10. (m>1)MENT -> ''
    11. (m>1)ENT -> ''
    12. ((m>1)and(*S or *Y))ION -> ''
    13. (m>1)OU -> ''
    14. (m>1)ISM -> ''
    15. (m>1)ATE -> ''
    16. (m>1)ITI -> ''
    17. (m>1)OUS -> ''
    18. (m>1)IVE -> ''
    19. (m>1)IZE -> ''
    '''

    # zipped_one_plus_suffix_consider = zip(from_one_plus_suffix_consider,
    #                             to_one_plus_suffix_consider)

    for suffix in from_one_plus_suffix_consider:
        if len(input_str) > len(suffix) + 1:

            if suffix == 'ion':
                if (input_str[-4] == 'y' or input_str[-4] == 's') and len(input_str) > 4:
                    input_str = input_str[0: len(
                        input_str) - len(suffix)]
                    continue
            if input_str.endswith(suffix):
                input_str = input_str[0: len(
                    input_str) - len(suffix)]

    return input_str
