from server_handler import ServerHandler

if __name__ == '__main__':
    """Sample testing"""
    server = ServerHandler()
    print(server.start())
    print(server.run_file("C:/Users/Matt/Dev/CS52-Autograder/serve-sml/example_sml/sample_assignment.sml"))
    print(server.run_file("C:/Users/Matt/Dev/CS52-Autograder/serve-sml/example_sml/simple_test.sml"))
    print(server.run_file("C:/Users/Matt/Dev/CS52-Autograder/serve-sml/example_sml/simple_test_2.sml"))
    print(server.get_results("1"))