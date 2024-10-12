class RankManager:
    def __init__(self, sb_manager):
        self._sb_manager = sb_manager

    @staticmethod
    def compute_score_list(traceback_function_name_list):
        scores = []
        for j in range(len(traceback_function_name_list)):
            item = (traceback_function_name_list[j], float(1) / (j + 1))
            scores.append(item)

        return scores

    def get_sorted_score_list(self, top_n: int):
        if top_n == -1:
            scored_function_list = self._sb_manager.select_all_ranked_functions()
        elif top_n >= 1:
            scored_function_list = self._sb_manager.select_top_n_ranked_functions(top_n)
        else:
            raise Exception(f"TopN {top_n} is not supported.")

        return scored_function_list
