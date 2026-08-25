"""消息常量：所有成功/失败提示集中管理，避免散落在业务代码中。"""

# ---- 成功 ----
SUCCESS_DELETE_BOOK = "删除成功"

# ---- 失败（书相关）----
FAIL_BOOK_NOT_FOUND = "id={book_id} 的书不存在"
FAIL_BOOK_ALREADY_BORROWED = "id={book_id} 的书已被借出"
FAIL_BOOK_NOT_BORROWED = "id={book_id} 的书还未借出"
