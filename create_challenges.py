import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'code_assistant_platform.settings')
django.setup()

from coding_assistant.models import CodingChallenge

def create_challenges():
    challenges = [
        {
            'title': 'Palindrome Checker',
            'description': 'Write a function `is_palindrome(s)` that checks if a given string `s` is a palindrome. A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward (ignoring spaces, punctuation, and capitalization).',
            'difficulty': 'BEGINNER',
            'starter_code': 'def is_palindrome(s):\n    # Your code here\n    pass',
            'solution': 'def is_palindrome(s):\n    s = "".join(c.lower() for c in s if c.isalnum())\n    return s == s[::-1]',
            'tags': 'string,algorithms'
        },
        {
            'title': 'FizzBuzz',
            'description': 'Write a program that prints the numbers from 1 to 100. But for multiples of three print "Fizz" instead of the number and for the multiples of five print "Buzz". For numbers which are multiples of both three and five print "FizzBuzz".',
            'difficulty': 'BEGINNER',
            'starter_code': 'def fizzbuzz(n):\n    # Your code here\n    pass',
            'solution': 'def fizzbuzz(n):\n    results = []\n    for i in range(1, n + 1):\n        if i % 3 == 0 and i % 5 == 0:\n            results.append("FizzBuzz")\n        elif i % 3 == 0:\n            results.append("Fizz")\n        elif i % 5 == 0:\n            results.append("Buzz")\n        else:\n            results.append(str(i))\n    return results',
            'tags': 'math,logic'
        },
        {
            'title': 'Two Sum',
            'description': 'Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. You may assume that each input would have exactly one solution, and you may not use the same element twice.',
            'difficulty': 'INTERMEDIATE',
            'starter_code': 'def two_sum(nums, target):\n    # Your code here\n    pass',
            'solution': 'def two_sum(nums, target):\n    prev_map = {}\n    for i, n in enumerate(nums):\n        diff = target - n\n        if diff in prev_map:\n            return [prev_map[diff], i]\n        prev_map[n] = i\n    return []',
            'tags': 'array,hash-table'
        }
    ]
    
    print(f"Creating {len(challenges)} challenges...")
    
    for data in challenges:
        challenge, created = CodingChallenge.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
        if created:
            print(f"Created: {challenge.title}")
        else:
            print(f"Already exists: {challenge.title}")
            
    print("Done!")

if __name__ == '__main__':
    create_challenges()
