from catty.words import (
    dupN,
    dup,
    dup2,
    dup3,
    swap,
    over,
    under,
    nip,
    tuck,
    slide,
    snip,
    drop,
    drop2,
    drop3,
    dropN,
    hide,
    reveal,
    depth,
    copy_stack,
    set_stack,
    save,
    restore
)
from . import check_reduce, check_error


def test_dupN_happy():
    check_reduce([0, 1, 2, 3, 4, dupN], [0, 1, 2, 3, 0, 1, 2, 3])


def test_dupN_warn0():
    check_reduce([2, 3, 0, dupN], [2, 3], [RuntimeWarning])


def test_dupN_missing():
    check_error([dupN], IndexError)


def test_dupN_not_int():
    check_error([1, 2, "asdf", dupN], ValueError)


def test_dupN_insufficient_data():
    check_error([1, 2, 3, dupN], IndexError)


def test_dup_happy():
    check_reduce([0, 3, dup], [0, 3, 3])


def test_dup_missing():
    check_error([dup], IndexError)


def test_dup2_happy():
    check_reduce([3, 4, dup2], [3, 4, 3, 4])


def test_dup2_missing():
    check_error([1, dup2], IndexError)


def test_dup3_happy():
    check_reduce([1, 2, 3, dup3], [1, 2, 3, 1, 2, 3])


def test_dup3_missing():
    check_error([1, dup3], IndexError)
    check_error([1, 2, dup3], IndexError)


def test_swap_happy():
    check_reduce([4, 9, swap], [9, 4])


def test_swap_missing_both():
    check_error([swap], IndexError)


def test_swap_missing_one():
    check_error([1, swap], IndexError)


def test_over_happy():
    check_reduce([1, 2, over], [1, 2, 1])


def test_over_missing_both():
    check_error([over], IndexError)


def test_over_missing_one():
    check_error([1, over], IndexError)


def test_under_happy():
    check_reduce([0, 1, 2, under], [0, 1, 1, 2])


def test_under_missing_both():
    check_error([under], IndexError)


def test_under_missing_one():
    check_error([1, under], IndexError)


def test_nip_happy():
    check_reduce([1, 2, nip], [2])


def test_nip_missing_both():
    check_error([nip], IndexError)


def test_nip_missing_one():
    check_error([1, nip], IndexError)


def test_tuck_happy():
    check_reduce([1, 2, 3, tuck], [3, 1, 2])


def test_tuck_missing():
    check_error([2, 3, tuck], IndexError)


def test_slide_happy():
    check_reduce([3, 1, 2, slide], [1, 2, 3])


def test_slide_missing():
    check_error([3, 1, slide], IndexError)


def test_snip_happy():
    check_reduce([1, 2, 3, snip], [2, 3])


def test_snip_missing():
    check_error([2, 3, snip], IndexError)


def test_dropN_happy():
    check_reduce([1, 2, 3, 4, 3, dropN], [1])


def test_dropN_invalid_N():
    check_error([1, "1", dropN], ValueError)


def test_dropN_no_N():
    check_error([dropN], IndexError)


def test_dropN_missing_data():
    check_error([1, 2, 3, dropN], IndexError)


def test_drop_happy():
    check_reduce([1, 2, drop], [1])


def test_drop_missing():
    check_error([drop], IndexError)


def test_drop2_happy():
    check_reduce([1, 2, 3, drop2], [1])


def test_drop2_missing():
    check_error([1, drop2], IndexError)


def test_drop3_happy():
    check_reduce([1, 2, 3, 4, drop3], [1])


def test_drop3_missing():
    check_error([1, 2, drop3], IndexError)


def test_hide_happy():
    check_reduce([1, 2, 3, 4, 5, hide], [5, 1, 2, 3, 4])


def test_hide_missing():
    check_error([hide], IndexError)


def test_reveal_happy():
    check_reduce([5, 1, 2, 3, 4, reveal], [1, 2, 3, 4, 5])


def test_reveal_missing():
    check_error([reveal], IndexError)


def test_depth_0():
    check_reduce([depth], [0])


def test_depth_happy():
    check_reduce([1, 2, 3, depth], [1, 2, 3, 3])


def test_copy_stack_happy():
    check_reduce([1, 2, 3, copy_stack], [1, 2, 3, [1, 2, 3]])


def test_copy_stack_empty():
    check_reduce([copy_stack], [[]])


def test_set_stack_list():
    check_reduce([3, 4, 5, [10, 11], set_stack], [10, 11])


def test_set_stack_iterable():
    check_reduce([10, 11, range(5), set_stack, 28], [0, 1, 2, 3, 4, 28])


def test_set_stack_string():
    check_reduce([10, 11, "asdf", set_stack], ["a", "s", "d", "f"])


def test_set_stack_missing():
    check_error([set_stack], IndexError)


def test_set_stack_invalid():
    check_error([None, set_stack], ValueError)


def test_save_happy():
    check_reduce([1, 2, 3, save], [[1, 2, 3], 1, 2, 3])


def test_save_empty():
    check_reduce([save], [[]])


def test_restore_happy():
    check_reduce([[1, 2, 3], 8, 9, restore], [1, 2, 3])


def test_restore_missing():
    check_error([restore], IndexError)


def test_restore_invalid():
    check_error([None, 1, 2, 3, restore], ValueError)
