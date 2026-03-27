from .BaseRoutingProtocol import BaseRoutingProtocol
import numpy as np

class AODVRouting(BaseRoutingProtocol):
    def __init__(self, field):
        super().__init__(field)
        self.routing_table = {}

    def setup_routing(self):
        """AODV 라우팅 프로토콜 기반 라우팅 테이블 설정"""
        # 실제 AODV는 on-demand 방식이지만, 여기서는 간단히 모든 노드에 대해 경로를 미리 설정
        for node_id in self.field.nodes:
            if node_id == 'BS':
                continue
            path = self._find_aodv_path(node_id, 'BS')
            if path:
                # next_hop은 경로의 두 번째 노드
                next_hop = path[1] if len(path) > 1 else 'BS'
                self.field.nodes[node_id].next_hop = next_hop
                self.field.nodes[node_id].hop_count = len(path) - 1
                self.routing_table[node_id] = next_hop
            else:
                self.field.nodes[node_id].next_hop = None
                self.field.nodes[node_id].hop_count = float('inf')
                self.routing_table[node_id] = None

    def _find_aodv_path(self, source_id, target_id):
        """AODV 방식의 경로 탐색 (여기서는 BFS로 단순화)"""
        if source_id not in self.field.nodes:
            return None
        queue = [(source_id, [source_id])]
        visited = set([source_id])
        while queue:
            current_id, path = queue.pop(0)
            if current_id == target_id or (target_id == 'BS' and self.field.nodes[current_id].next_hop == 'BS'):
                if target_id == 'BS' and self.field.nodes[current_id].next_hop == 'BS':
                    return path + ['BS']
                return path
            current_node = self.field.nodes[current_id]
            for neighbor_id in getattr(current_node, 'neighbor_nodes', []):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))
        return None
