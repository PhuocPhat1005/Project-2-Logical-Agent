from pysat.formula import (
    CNF,
)  # Nhập lớp CNF từ thư viện PySAT, dùng để xử lý các công thức ở dạng chuẩn tắc liên hợp (CNF).
from pysat.solvers import (
    Solver,
)  # Nhập lớp Solver từ PySAT, dùng để giải các bài toán SAT.


class KnowledgeBase:
    def __init__(self):
        self.formula = (
            CNF()
        )  # Khởi tạo một công thức CNF mới, sẽ chứa cơ sở tri thức dưới dạng danh sách các mệnh đề.

    @staticmethod
    def standardize_clause(clause):
        """
        Chuẩn hóa một mệnh đề bằng cách loại bỏ các phần tử trùng lặp và sắp xếp nó.

        :param clause: Một danh sách đại diện cho một mệnh đề (là sự kết hợp của các literal).
        :return: Mệnh đề đã được chuẩn hóa (đã sắp xếp và không có phần tử trùng lặp).
        """
        return sorted(
            list(set(clause))
        )  # Chuyển mệnh đề thành một tập hợp để loại bỏ các phần tử trùng lặp, sau đó sắp xếp nó.

    def add_clause(self, clause):
        """
        Thêm một mệnh đề đã chuẩn hóa vào cơ sở tri thức.

        :param clause: Một danh sách đại diện cho một mệnh đề cần thêm vào.
        """
        clause = self.standardize_clause(clause)  # Chuẩn hóa mệnh đề.
        if (
            clause not in self.formula
        ):  # Kiểm tra nếu mệnh đề chưa có trong cơ sở tri thức.
            self.formula.append(clause)  # Thêm mệnh đề vào công thức CNF.

    def del_clause(self, clause):
        """
        Xóa một mệnh đề đã chuẩn hóa khỏi cơ sở tri thức.

        :param clause: Một danh sách đại diện cho một mệnh đề cần xóa.
        """
        clause = self.standardize_clause(clause)  # Chuẩn hóa mệnh đề.
        if clause in self.formula:  # Kiểm tra nếu mệnh đề có trong cơ sở tri thức.
            self.formula.remove(clause)  # Xóa mệnh đề khỏi công thức CNF.

    def infer(self, not_alpha):
        """
        Thực hiện suy diễn logic dựa trên cơ sở tri thức hiện tại.

        :param not_alpha: Một danh sách các mệnh đề đại diện cho phủ định của công thức bạn muốn kiểm tra.
        :return: Trả về True nếu công thức được suy diễn (not_alpha không thể thỏa mãn); False nếu không.
        """
        with Solver(
            bootstrap_with=self.formula
        ) as solver:  # Khởi tạo bộ giải SAT với cơ sở tri thức hiện tại.
            for clause in not_alpha:  # Lặp qua từng mệnh đề trong not_alpha.
                if not isinstance(
                    clause, list
                ):  # Đảm bảo rằng mệnh đề ở dạng danh sách.
                    clause = [clause]
                solver.add_clause(clause)  # Thêm mệnh đề vào bộ giải.
            return (
                not solver.solve()
            )  # Nếu bộ giải không thể tìm ra lời giải, trả về True (có sự suy diễn).
