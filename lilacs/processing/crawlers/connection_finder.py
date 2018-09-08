from lilacs.processing.crawlers import BaseCrawler
from lilacs.data_sources.conceptnet import extract_conceptnet_connections
from lilacs.data_sources.wordnet import extract_wordnet_connections
from lilacs.data_sources.dictionary import extract_dictionary_connections


class ConnectionFinderCrawler(BaseCrawler):
    def execute_action(self, connections):
        print("** current", self.current_node.name)
        # execute an action in current node
        new_cons = []
        # extract new connections from conceptnet
        cons = extract_conceptnet_connections(self.current_node.name)
        for con_type, target, strength in cons:
            if not self.con_exists(con_type, self.current_node.name, target):
                c = self.db.add_connection(self.current_node.name, target, con_type, strength=strength)
                if c is not None:
                    new_cons.append(c)

        # extract new connections from wordnet
        cons = extract_wordnet_connections(self.current_node.name)
        for con_type, target, strength in cons:
            if not self.con_exists(con_type, self.current_node.name, target):
                c = self.db.add_connection(self.current_node.name, target, con_type, strength=strength)
                if c is not None:
                    new_cons.append(c)

        # extract new connections from dictionary
        cons = extract_dictionary_connections(self.current_node.name)
        for con_type, target, strength in cons:
            if not self.con_exists(con_type, self.current_node.name, target):
                c = self.db.add_connection(self.current_node.name, target, con_type, strength=strength)
                if c is not None:
                    new_cons.append(c)
            if con_type in ["synonym", "antonym"]:
                if not self.con_exists(con_type, target, self.current_node.name):
                    c = self.db.add_connection(target, self.current_node.name, con_type, strength=strength)
                    if c is not None:
                        new_cons.append(c)

        return new_cons


if __name__ == "__main__":
    c = ConnectionFinderCrawler(threaded=False)
    c.start_crawling("person")
    print(c.crawl_list)
    print(c.total_steps)