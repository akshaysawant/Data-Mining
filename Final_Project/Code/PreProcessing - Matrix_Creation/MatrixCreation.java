import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.StringTokenizer;
import org.tartarus.snowball.EnglishSnowballStemmerFactory;
import org.tartarus.snowball.util.StemmerException;

public class MatrixCreation {

    static Set<String> stopWord;
    static Set<String> specialCharacters;

    public static void main(String args[]) throws IOException {
        try {
            // Initialize stop words and special character
	    initializeStopWording();
            initializeSpecialCharacters();
            
            BufferedReader reader;
            File file = new File(args[1]);
            BufferedWriter writer = new BufferedWriter(new FileWriter(file));

            String[] Authors;
            String author_string = "";
            String allcsa = "";
            String[][] data_matrix = new String[1][8];

            reader = new BufferedReader(new FileReader(args[0]));

            int row = 0;
            int column = 0;
            String this_line = "";
            this_line = reader.readLine();

	    // Read the data line by line
            while (this_line != null) {
                author_string = "";
                Authors = null;
                allcsa = "";
                if (this_line.startsWith("#")) {
                    String start2;
                    start2 = this_line.substring(0, 2);
                    switch (start2) {
                        case "#i": // index
                            column = 0;
                            data_matrix[row][column] = this_line.substring(6).trim();
                            break;
                        case "#*": //title 
                            column = 1;
                            data_matrix[row][column] = processString(this_line.substring(2).trim());
                            break;
                        case "#@": // Author
                            column = 2;
                            author_string = this_line.substring(2);
                            Authors = author_string.split(";");
                            for (String a : Authors) {
                                a = a.trim();
                                if (allcsa != null) {
                                    if (a != null) {
                                        allcsa += a + ",";
                                    }
                                } else {
                                    if (a != null) {
                                        allcsa = a + ",";
                                    }

                                }
                            }
                            data_matrix[row][column] = allcsa.substring(0, allcsa.length() - 1);
                            break;
                        case "#t": // year
                            column = 3;
                            data_matrix[row][column] = this_line.substring(2).trim();
                            break;
                        case "#c": // venue
                            column = 4;
                            data_matrix[row][column] = processString(this_line.substring(2).trim());
                            break;
                        case "#%": // References
                            column = 5;
                            if (data_matrix[row][column] != null) {
                                data_matrix[row][column] += "," + this_line.substring(2).trim();
                            } else {
                                data_matrix[row][column] = this_line.substring(2).trim();
                            }
                            break;
                        case "#!": // Abstract
                            column = 6;
                            data_matrix[row][column] = processString(this_line.substring(2).trim());
                            break;
                    }

                } else {
                    if (data_matrix != null) {
			// When one entry is completed we write that entry
                        for (int i = 0; i < 7; i++) {
                            if (data_matrix[row][i] != null) {
                                writer.write(data_matrix[row][i].toLowerCase() + ";");
                            } else {
                                writer.write(";");
                            }
                        }
                        writer.newLine();
                        data_matrix = new String[1][8];
                    }
                }

                this_line = reader.readLine();

            }

            writer.flush();
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    private static String removeSpecialCharacters(String content) {
        String token;
        String processed = "";
        StringTokenizer st = new StringTokenizer(content);
        while (st.hasMoreTokens()) {
            token = st.nextToken();
            for (String character : specialCharacters) {
                if (token.contains(character)) {
                    token = token.replace(character, " ");
                }
            }
            processed += token.trim() + " ";
        }
        return processed.trim();
    }

    // This method applies stop wording, stemming and removes special
    // characters from the input string. Also it converts the input string
    // to lower case so case mismatch doesn't remain an issue further
    private static String processString(String content) {
        StringTokenizer st;
        st = new StringTokenizer(content);
        String token;
        String processed = "";
        String tokenCopy;
        String charToStr;
        EnglishSnowballStemmerFactory stemmer = EnglishSnowballStemmerFactory.getInstance();
        while (st.hasMoreTokens()) {
            try {
                token = st.nextToken().toLowerCase().trim();
                token = stemmer.process(token.trim());
                token = new String(token.getBytes(), "UTF-8");
                if (!stopWord.contains(token) && !token.matches("\\d+")) {
                    tokenCopy = token;
                    token = "";

                    for (char character : tokenCopy.toCharArray()) {
                        charToStr = Character.toString(character);
                        if (!specialCharacters.contains(charToStr)) {
                            token += charToStr;
                        }
                    }
                    processed += token.trim() + " ";
                }
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
        return processed.trim();
    }

    private static void initializeStopWording() throws StemmerException {
        File file = new File("Files/stopwords.txt");
        BufferedReader reader = null;
        StringTokenizer st;
        String line;
        EnglishSnowballStemmerFactory stemmer = EnglishSnowballStemmerFactory.getInstance();
        try {
            reader = new BufferedReader(new FileReader(file));
            stopWord = new HashSet();
            String token;
            while ((line = reader.readLine()) != null) {
                if (line.contains(";")) {
                    st = new StringTokenizer(";");
                    while (st.hasMoreTokens()) {
                        token = stemmer.process(st.nextToken().trim().toLowerCase());
                        stopWord.add(new String(token.getBytes(), "UTF-8"));
                    }
                } else {
                    token = stemmer.process(line.trim().toLowerCase());
                    stopWord.add(new String(token.getBytes(), "UTF-8"));
                }
            }
        } catch (FileNotFoundException ex) {
        } catch (IOException ex) {
        } finally {
            try {
                reader.close();
            } catch (IOException ex) {
            }
        }
    }

    private static void initializeSpecialCharacters() {
        File file = new File("Files/specialcharacters.txt");
        BufferedReader reader = null;
        String line;
        try {
            reader = new BufferedReader(new FileReader(file));
            specialCharacters = new HashSet();
            while ((line = reader.readLine()) != null) {
                specialCharacters.add(new String(line.trim().getBytes(), "UTF-8"));
            }
        } catch (FileNotFoundException ex) {
        } catch (IOException ex) {
        } finally {
            try {
                reader.close();
            } catch (IOException ex) {
            }
        }
    }

}
