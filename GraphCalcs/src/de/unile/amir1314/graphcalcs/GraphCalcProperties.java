package de.unile.amir1314.graphcalcs;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class GraphCalcProperties {

	private static GraphCalcProperties instance;
	private Properties properties;

	private GraphCalcProperties() {
		properties = new Properties();
		try {
			BufferedInputStream stream = new BufferedInputStream(
					new FileInputStream("config.properties"));
			properties.load(stream);
			stream.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static GraphCalcProperties getGraphCalcProperties() {
		if (instance == null) {
			instance = new GraphCalcProperties();
		}
		return instance;
	}

	public Properties getProperties() {
		return properties;
	}

}
