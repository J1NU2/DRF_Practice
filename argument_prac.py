# def argument(num, *args, **kwargs):
#     print(f"num : {num}")
#     print(f"args : {args}")
#     print(f"kwargs :{kwargs}")

#     return argument


# argument(100, 1, 2, 3, 4, 5, num1=1, num2=2, num3=3)


def argument(num, *jinu, **racoon):
    print(f"num : {num}")
    print(f"jinu : {jinu}")
    print(f"racoon :{racoon}")

    return argument


argument(100, 1, 2, 3, 4, 5, num1=1, num2=2, num3=3)
