classDiagram
    %%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'primaryBorderColor': '#3174f1', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'fontFamily': 'sans-serif'}}}%%

    %% Field 클래스
    class Field {
        +width: float
        +height: float
        +nodes: dict
        +base_station: dict
        +deploy_nodes(num_nodes)
        +set_base_station(x, y)
        +find_neighbors()
    }
    
    %% core/nodes 모듈
    class Sensors {
        <<abstract>>
        +node_id: int
        +pos_x, pos_y: float
        +status: string
        +node_type: string
        +next_hop: int
        +hop_count: float
        +calculate_distance_to_bs(bs_x, bs_y)
    }
    
    class MicazMotes {
        +comm_range: float
        +energy_level: float
        +initial_energy: float
        +transmit_packet(packet_size)
        +receive_packet(packet_size)
    }
    
    %% 라우팅 관련 클래스
    class BaseRoutingProtocol {
        <<abstract>>
        +field: Field
        +setup_routing()
        +get_path_to_bs(node_id)
        +simulate_reports(num_reports)
    }
    
    class DijkstraRouting {
        +setup_routing()
        +connect_direct_to_bs()
        +apply_dijkstra_routing()
    }

    %% 추가된 AODVRouting 클래스
    class AODVRouting {
        +routing_table: dict
        +setup_routing()
        +find_aodv_path(source_id, target_id)
    }
    
    %% attacks 모듈
    class NetworkAttackBase {
        <<abstract>>
        +field: Field
        +attack_type: string
        +attack_range: int
        +malicious_nodes: list
        +execute_attack(num_attackers)
    }
    
    class Sinkhole {
        +int grid_size
        +calculate_node_density()
        +execute_attack(num_attackers)
        +launch_outside_attack(num_attackers)
        +launch_inside_attack(num_attackers)
    }
    
    %% 시뮬레이션 모듈
    class WsnSimulation {
        +simulate_with_attack(field, routing, attack_timing, num_reports)
        +plot_wsn_network(field, classified_nodes)
        +get_routing_protocol(protocol_name, field)
    }
    
    %% 관계 설정
    Field *-- Sensors
    Sensors <|-- MicazMotes
    
    Field <-- BaseRoutingProtocol
    BaseRoutingProtocol <|-- DijkstraRouting
    BaseRoutingProtocol <|-- AODVRouting
    
    Field <-- NetworkAttackBase
    NetworkAttackBase <|-- Sinkhole
    
    WsnSimulation ..> Field
    WsnSimulation ..> BaseRoutingProtocol
    WsnSimulation ..> Sinkhole