from fauxpy.fault_localization.mbfl.db_manager import MbflDbManager
from fauxpy.fault_localization.mbfl.metric_metallaxis import MetricMetallaxis
from fauxpy.fault_localization.mbfl.metric_muse import MetricMuse


class EntityScoreManager:
    def __init__(self, db_manager: MbflDbManager):
        self._db_manager = db_manager

    @staticmethod
    def _compute_entity_scores(mutant_score_list):
        muse_mutant_score_list = mutant_score_list["Muse"]
        metallaxis_mutant_scores = mutant_score_list["Metallaxis"]

        muse_entity_score = MetricMuse.compute_entity_score(muse_mutant_score_list)
        metallaxis_entity_score = MetricMetallaxis.compute_entity_score(
            metallaxis_mutant_scores
        )

        return {"Muse": muse_entity_score, "Metallaxis": metallaxis_entity_score}

    def compute_entity_scores_store_db(self, top_n: int):
        entities = self._db_manager.select_distinct_all_mutant_score_terms_entities()

        for entity in entities:
            mutant_scores = self._db_manager.select_mutant_score_terms_scores(entity)
            entity_scores = self._compute_entity_scores(mutant_scores)

            entity_muse_score = entity_scores["Muse"]
            entity_metallaxis_score = entity_scores["Metallaxis"]

            self._db_manager.insert_entity_score(
                entity, entity_muse_score, entity_metallaxis_score
            )

        if top_n == -1:
            score_entities = self._db_manager.select_all_ranked_entities()
        elif top_n >= 1:
            pass
            score_entities = self._db_manager.select_top_n_ranked_entities(top_n)
        else:
            raise Exception(f"TopN {top_n} is not supported.")

        return score_entities
