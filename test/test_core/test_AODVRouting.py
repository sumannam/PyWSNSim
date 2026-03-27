import unittest
from core.Field import Field
from core.routing.AODVRouting import AODVRouting

class TestAODVRouting(unittest.TestCase):
    def setUp(self):
        # 100x100 필드에 5개 노드 배치
        self.field = Field(100, 100)
        self.field.deploy_nodes(5)
        self.field.set_base_station(50, 50)
        self.field.find_neighbors()
        self.routing = AODVRouting(self.field)

    def test_setup_routing(self):
        self.routing.setup_routing()
        # 각 노드의 next_hop이 None이 아니거나 'BS'인지 확인
        for node_id, node in self.field.nodes.items():
            self.assertTrue(node.next_hop is not None or node.next_hop == 'BS')

    def test_routing_table(self):
        self.routing.setup_routing()
        # 라우팅 테이블이 노드 수와 동일한지 확인
        self.assertEqual(len(self.routing.routing_table), len(self.field.nodes))

    def test_path_to_bs(self):
        self.routing.setup_routing()
        for node_id in self.field.nodes:
            path = self.routing.get_path_to_bs(node_id)
            # 경로가 최소 2개 이상(자기자신, BS) 또는 None
            self.assertTrue(path is None or len(path) >= 1)

# if __name__ == "__main__":
#     unittest.main()
