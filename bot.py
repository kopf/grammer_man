#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import time
import pickle

import twitter

from grabber import get_spellings

API = twitter.Api()

MESSAGES = u'''
Hey $USERNAME, didn't you mean $CORRECT there?
$USERNAME bro, it's spelled $CORRECT.
Just helpin' out my pal $USERNAME - it's $CORRECT, not $MISTAKE.
$USERNAME. $CORRECT, not $MISTAKE. Just helpin out! ;Â¬}
Just lettin' you know it's spelled $CORRECT, not $MISTAKE, $USERNAME.
YO $USERNAME ------- $CORRECT NOT $MISTAKE... GET ME??
Hey $USERNAME, you may not be aware, but it's actually $CORRECT and not $MISTAKE !
Uhm, $USERNAME, have you tried using $CORRECT instead of $MISTAKE
Hi, uhhhh, so if you could go ahead and use $CORRECT here, $USERNAME, and not $MISTAKE, that'd be great, okay? Thanks
$USERNAME just wanted to point out that it's $CORRECT and not $MISTAKE have a nice day!!
Big up $USERNAME, but it's not $MISTAKE, it's $CORRECT yo.
$USERNAME try using $CORRECT instead of $MISTAKE next time!
Last place in the spelling bee, huh $USERNAME? Try $CORRECT instead of $MISTAKE next time, punk.
$USERNAME Didn't you go to school? Everyone knows it's $CORRECT and not $MISTAKE
Almost got it, $USERNAME, but it's actually $CORRECT rather than $MISTAKE
Heh! Easy one to make $USERNAME but it's $CORRECT, not $MISTAKE
You're making yourself look bad $USERNAME! $CORRECT, not $MISTAKE!
I've been watching you for a while, $USERNAME, and you keep spelling $CORRECT wrong! It's not $MISTAKE, jeez.
Just lettin' my main man $USERNAME know that it's $CORRECT, not $MISTAKE
Hi there $USERNAME! Try spelling $MISTAKE correctly next time, it's $CORRECT
Shame on you $USERNAME. $MISTAKE isn't a word, surely you know that.. try $CORRECT instead
Hey $USERNAME - You say potato, I say potato but everyone says $CORRECT, not $MISTAKE!
Haha $USERNAME, love how you spelled $CORRECT as $MISTAKE! Great one ;)
$USERNAME Hey gurl, shouldn't that be $CORRECT? :Â¬)
$USERNAME how could you misspell $CORRECT...everyone knows that one!
Lucky $USERNAME, I said $MISTAKE instead of $CORRECT at your age and saw the back of my da's hand.
OK $USERNAME, I know you got a crocodile in spelling, but you must know it is $CORRECT, not $MISTAKE.
Hanukkah can be spelled so many ways $USERNAME, but $MISTAKE is not the same as $CORRECT.
Hey $USERNAME, I've never seen $CORRECT spelled like that! Creative!
I hope English isn't $USERNAME's first language. $CORRECT, not $MISTAKE!
$USERNAME c'mon son! It's $CORRECT!!!
$USERNAME Hey man, it's $CORRECT, not $MISTAKE. Just sayin'!
$USERNAME sooo you might wanna spell $CORRECT the right way next time!! Not your fault bro.
Ah $USERNAME, in all fairness, it's $CORRECT, not $MISTAKE.
$MISTAKE is spelled $CORRECT, looks won't last forever $USERNAME! Learn to spell.
$USERNAME, thought you might wanna know it's spelled $CORRECT, not $MISTAKE! Guess you can call me a words freak <3
Yo $USERNAME, spelling tip of the day: it's $CORRECT not $MISTAKE!! Haha.
$USERNAME I know we don't know eachother well but you're killing me here - it's $CORRECT, yeah?
Come on $USERNAME, it's spelled $CORRECT, not $MISTAKE.
Nothing is worse than people spelling $CORRECT as $MISTAKE. C'mon $USERNAME.
Absolutely hate it when people spell $CORRECT $MISTAKE. Hang your head in shame, $USERNAME!
Congrats to $USERNAME for the most inventive spelling of $CORRECT i've seen in a while: $MISTAKE. Amazing!
$CORRECT, $USERNAME. $CORRECT.
$MISTAKE, $USERNAME? Seriously? It's $CORRECT.
Everyone knows you spell $MISTAKE $CORRECT.. Everyone except $USERNAME.
$USERNAME Spelling $CORRECT as $MISTAKE just makes my toes curl. 
Can't believe people are still making the mistake of writing $MISTAKE instead of $CORRECT. $USERNAME, I'm lookin' at you!
$USERNAME, any desire to do an evening class in English spelling? It's $CORRECT, not $MISTAKE.
$USERNAME $MISTAKE - seriously? Like, really? Learn to spell!
Best check a dictionary before taking to twitter again, $USERNAME. Might find out $MISTAKE is spelled $CORRECT.
$MISTAKE? Pretty embarrassing really, $USERNAME. It's actually $CORRECT.
Surely you're old enough to know $MISTAKE is spelled $CORRECT, $USERNAME..?
Don't you mean $CORRECT, $USERNAME?
It's unreal how often people manage to spell $CORRECT as $MISTAKE... Don't be one of them, $USERNAME!
Hope you remember that $MISTAKE is spelled $CORRECT in the future, $USERNAME.
$USERNAME, it's spelled $CORRECT. Just doin' my bit, helpin' out!
$USERNAME If I see one more person writing $MISTAKE instead of $CORRECT, I think I'm going to go mad.
'''.split('\n')

def compose_message(twitter_post, mistake, correct):
    '''
    Choose a message from MESSAGES at random, substitute fields to personalise it and 
    check if it exceeds the twitter message limit. Try this 100 times before failing.
    '''
    retries = 0
    while retries < 100:
        message = MESSAGES[random.randint(0, len(MESSAGES) - 1)]
        message = message.replace('$USERNAME', '@%s' % twitter_post.user.screen_name)
        message = message.replace('$MISTAKE', '"%s"' % mistake).replace('$CORRECT', '"%s"' % correct)
        if message and len(message) < 141:
            return message
    return None

def correct_spelling(twitter_post, mistake, correct):
    '''
    Correct someone's spelling in a twitter_post
    '''
    print u'Correcting @%s for using %s...' %(twitter_post.user.screen_name, 
                                            mistake)
    message = compose_message(twitter_post, mistake, correct)
    if not message:
        print u'All messages were too long... Aborting...'
        return False
    else:
        failures = 0
        try:
            API.PostUpdate(message, in_reply_to_status_id=twitter_post.id)
        except Exception, e:
            print 'Failed to submit tweet (%s).'
            return False
        return True

def search(word):
    '''
    Search twitter for uses of a word, return one if it's been used recently.
    Otherwise return None.
    
    TODO: Add time awareness.
    '''
    print 'Searching for uses of %s...' % word
    results = API.GetSearch(word)
    if results:
        for result in results:
            if not check_if_done(result.id) and not result.user.screen_name == 'grammer_man' and word in result.text:
                return result
    return None

def check_if_done(id):
    '''
    Checks if a tweet has already been responded to
    '''
    if os.path.exists('done.pkl'):
        f = open('done.pkl', 'r')
        done = pickle.load(f)
        f.close()
        if id in done:
            return True
    return False

def update_done(id):
    '''
    Updates a list of tweets that've been replied to
    '''
    if os.path.exists('done.pkl'):
        f = open('done.pkl', 'r')
        done = pickle.load(f)
        f.close()
    else:
        done = []
    
    done.append(id)
    
    f = open('done.pkl', 'w')
    pickle.dump(done, f)
    f.close()

def main():
    '''
    Main program flow
    '''
    words = get_spellings()
    counter = 0 
    while True:
        word = random.choice(words.keys())
        post = search(word)
        if counter > 100:
            rand_time = random.randint(120*60, 240*60)
            print 'Done %s tweets, sleeping for %s minutes' % (counter, rand_time/60)
            time.sleep(rand_time)
            counter = 0
        # TODO: PROPERLY PRUNE THE MISTAKES/CORRECTIONS FROM WIKIPEDIA AND REMOVE THIS:
        if not u',' in word + words[word] and not u';' in word + words[word]:
            if post:
                result = correct_spelling(post, word, words[word])
                if result:
                    counter += 1
                    print '#%s Done' % counter
                    update_done(post.id)
                    time.sleep(random.randint(300,500))
            

if __name__ == '__main__':
    main()
