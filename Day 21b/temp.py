#
# # top left
# row_length = 65
# area = 0
# calculated_corners_odd = [set(), set(), set(), set()]
# calculated_corners_even = [set(), set(), set(), set()]
# for y in range(0, 65):
#     line = ""
#     for x in range(0, row_length):
#         area += 1
#         if (y,x) in main_visitable_squares_even:
#             even_corners_walkable[0] += 1
#             calculated_corners_even[0].add((y, x))
#
#             if (y, x) not in even_corners[0]:
#                 raise ValueError('More than 65')
#
#         elif (y,x) in main_visitable_squares_odd:
#             odd_corners_walkable[0] += 1
#             calculated_corners_odd[0].add((y,x))
#
#             if (y, x) not in odd_corners[0]:
#                 raise ValueError('More than 65')
#
#         line += yard[y][x]
#
#     row_length -= 1
#     #print(f"{y}: {line}")
# print(f"Area was {area}\n")
#
# if calculated_corners_even[0] != even_corners[0]:
#     raise ValueError('Difference in calc')
# elif calculated_corners_odd[0] != odd_corners[0]:
#     raise ValueError('Difference in calc')
#
# # top right
# area = 0
# for y in range(0, 65):
#     line = ""
#     for x in range(66+y, 131):
#         area += 1
#         if (y,x) in main_visitable_squares_even:
#             even_corners_walkable[1] += 1
#         elif (y,x) in main_visitable_squares_odd:
#             odd_corners_walkable[1] += 1
#         line += yard[y][x]
#     row_length -= 1
#     #print(f"{y}: {line}")
# print(f"Area was {area}\n")
#
# # bottom right
# row_length = 1
# area = 0
# for y in range(66, 131):
#     line = ""
#     for x in range(130, 130-row_length, -1):
#         area += 1
#         if (y,x) in main_visitable_squares_even:
#             even_corners_walkable[2] += 1
#         elif (y,x) in main_visitable_squares_odd:
#             odd_corners_walkable[2] += 1
#         line += yard[y][x]
#     row_length += 1
#     #print(f"{y}: {line}")
# print(f"Area was {area}\n")
#
# # bottom left
# row_length = 1
# area = 0
# for y in range(66, 131):
#     line = ""
#     for x in range(0, row_length):
#         area += 1
#         if (y,x) in main_visitable_squares_even:
#             even_corners_walkable[3] += 1
#         elif (y,x) in main_visitable_squares_odd:
#             odd_corners_walkable[3] += 1
#         line += yard[y][x]
#     row_length += 1
#     #print(f"{y}: {line}")
# print(f"Area was {area}\n")