package de.unile.amir1314.graphcalcs;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Relationship;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;

import au.com.bytecode.opencsv.CSVReader;

public class Main {

	private static Map<String, Node> wordnodes = new HashMap<>();
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// setup db
		Properties props = GraphCalcProperties.getGraphCalcProperties()
				.getProperties();
		String DB_PATH = props.getProperty("DB_PATH");
		GraphDatabaseService graphDb = new GraphDatabaseFactory()
				.newEmbeddedDatabase(DB_PATH);
		registerShutdownHook(graphDb);

		setupDB(graphDb, "test.csv");
		// end program
		graphDb.shutdown();

	}

	private static void setupDB(GraphDatabaseService graphDb, String filepath) {
		CSVReader reader;;
		try {
			reader = new CSVReader(new FileReader(filepath));
			String[] nextLine;
			try (Transaction tx = graphDb.beginTx()) {
				while ((nextLine = reader.readNext()) != null) {
					Node from = getWordNode(graphDb,
							nextLine[0]);
					Node to = getWordNode(graphDb,
									nextLine[1]);
					Relationship r = from.createRelationshipTo(to,
							RelationTypes.OCCURS_WITH);
					r.setProperty("value", Double.parseDouble(nextLine[2]));
					tx.success();
				}
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private static Node getWordNode(GraphDatabaseService db, String word) {
		if( wordnodes.containsKey(word)) return wordnodes.get(word);
		Node node = db.createNode();
		node.setProperty("word", word);
		wordnodes.put(word, node);
		return node;
	}

	private static void registerShutdownHook(final GraphDatabaseService graphDb) {
		// Registers a shutdown hook for the Neo4j instance so that it
		// shuts down nicely when the VM exits (even if you "Ctrl-C" the
		// running application).
		Runtime.getRuntime().addShutdownHook(new Thread() {
			@Override
			public void run() {
				graphDb.shutdown();
			}
		});
	}

}
