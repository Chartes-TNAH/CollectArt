-- Données tests de la base SQLite pour CollectArt

INSERT INTO `collection` (
	`collection_name`, `collection_collector_name`, `collection_collector_firstname`, `collection_collector_date`, `collection_collector_bio`)
VALUES 
("Collection Paets", "Paets I", "Adriaen", "1631-1686", "Régent de Rotterdam, directeur de la Compagnie néerlandaise des Indes orientales et ambassadeur en Espagne et en Angleterre."),
("Collection Bolnes", "Bolnes", "Catharina", "1631-1687", "Collectionneuse catholique aisée — issue par sa mère, Maria Thins, d’une riche famille de marchands de briques de Gouda —, mariée au peintre Johannes Vermeer."),
("Collection Duarte", "Duarte", "Diego", "1612-1691", "Joaillier banquier, compositeur et collectionneur d'art portugais vivant à Anvers."),
("Collection Ruijiven", "Claesz von Ruijiven", "Pieter", "1624-1674", "Principal mécène du peintre Johannes Vermeer.");

INSERT INTO `mediums` (
	`label`) 
VALUES 
("peinture"),
("sculpture"),
("gravure"),
("dessin"),
("objet d'art"),
("photographie");

INSERT INTO `work` (
	`work_title`, `work_author`, `work_date`, `work_medium`, `work_dimensions`, `work_image_lien`, `work_collection_id`) 
VALUES 
("The Astronomer", "Johannes Vermeer", "1668", "peinture", "50 x 45 cm", "https://upload.wikimedia.org/wikipedia/commons/0/0e/Johannes_Vermeer_-_The_Astronomer_-_WGA24685.jpg", 1),
("The Geographer", "Johannes Vermeer", "1669", "peinture", "50 x 46,6 cm", "https://upload.wikimedia.org/wikipedia/commons/9/9b/Jan_Vermeer_-_The_Geographer.JPG", 1),
("The Guitar Player", "Johannes Vermeer", "1671-1672", "peinture", "53 x 46,3 cm", "https://upload.wikimedia.org/wikipedia/commons/7/70/Jan_Vermeer_van_Delft_013.jpg", 2),
("Lady Writing a Letter with her Maid", "Johannes Vermeer", "vers 1670", "peinture", "71,1 x 58,4 cm", "https://upload.wikimedia.org/wikipedia/commons/4/44/Woman_writing_a_letter%2C_with_her_maid%2C_by_Johannes_Vermeer.jpg", 2),
("The Art of Painting", "Johannes Vermeer", "vers 1666-1668", "peinture", "120 x 100 cm", "https://upload.wikimedia.org/wikipedia/commons/5/5e/Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg", 2),
("Young Woman Seated at a Virginal", "Johannes Vermeer", "vers 1670-1672", "peinture", "51,5 x 45,5 cm", "https://upload.wikimedia.org/wikipedia/commons/5/55/Lady_Seated_at_a_Virginal%2C_Vermeer%2C_The_National_Gallery%2C_London.jpg", 3),
("Young Woman Standing at a Virginal", "Johannes Vermeer", "vers 1670-1672", "peinture", "52 x 45 cm", "https://upload.wikimedia.org/wikipedia/commons/3/3d/Jan_Vermeer_van_Delft_-_Lady_Standing_at_a_Virginal_-_National_Gallery%2C_London.jpg", 3),
("A Lady Writing", "Johannes Vermeer", "vers 1665", "peinture", "45 x 39,9 cm", "https://upload.wikimedia.org/wikipedia/commons/2/21/Johannes_Vermeer_-_A_lady_writing_%28c_1665-1666%29.jpg", 4),
("A Lady at the Virginal with a Gentleman", "Johannes Vermeer", "vers 1662-1665", "peinture", "73,3 x 64,5 cm", "https://upload.wikimedia.org/wikipedia/commons/b/bc/Johannes_Vermeer_-_Lady_at_the_Virginal_with_a_Gentleman%2C_%27The_Music_Lesson%27_-_Google_Art_Project.jpg", 4),
("A Maid Asleep", "Johannes Vermeer", "vers 1656-1657", "peinture", "87,6 x 76,5 cm", "https://upload.wikimedia.org/wikipedia/commons/2/2f/Vermeer_young_women_sleeping.jpg", 4),
("A View of Delft", "Johannes Vermeer", "vers 1660-1661", "peinture", "98,5 x 117,5 cm", "https://upload.wikimedia.org/wikipedia/commons/e/ed/View_of_Delft%2C_by_Johannes_Vermeer.jpg", 4),
("Girl with a Pearl Earring", "Johannes Vermeer", "vers 1665-1666", "peinture", "46,5 x 40 cm", "https://upload.wikimedia.org/wikipedia/commons/c/ce/Girl_with_a_Pearl_Earring.jpg", 4),
("Girl with a Red Hat", "Johannes Vermeer", "vers 1665-1667", "peinture", "23,2 x 18,1 cm", "https://upload.wikimedia.org/wikipedia/commons/a/a3/Vermeer_-_Girl_with_a_Red_Hat.JPG", 4),
("Mistress and Maid", "Johannes Vermeer", "vers 1665-1670", "peinture", "90,2 x 78,7 cm", "https://upload.wikimedia.org/wikipedia/commons/6/61/Vermeer_Lady_Maidservant_Holding_Letter.jpg", 4),
("Officer and Laughing Girl", "Johannes Vermeer", "vers 1655-1660", "peinture", "50,5 x 46 cm", "https://upload.wikimedia.org/wikipedia/commons/b/bd/Johannes_Vermeer_-_Officer_with_a_Laughing_Girl_-_WGA24622.jpg", 4),
("Study of a Young Woman", "Johannes Vermeer", "vers 1666-1667", "peinture", "44,5 x 40 cm", "https://upload.wikimedia.org/wikipedia/commons/d/d9/Vermeer-Portrait_of_a_Young_Woman.jpg", 4),
("The Concert", "Johannes Vermeer", "vers 1665-1666", "peinture", "72,5 x 64,7 cm", "https://upload.wikimedia.org/wikipedia/commons/7/7f/Vermeer_The_Concert.jpg", 4),
("The Girl with the Wine Glass", "Johannes Vermeer", "vers 1659-1660", "peinture", "78 x 67 cm", "https://upload.wikimedia.org/wikipedia/commons/1/1f/Jan_Vermeer_van_Delft_006.jpg", 4),
("The Lacemaker", "Johannes Vermeer", "vers 1669-1670", "peinture", "24,5 x 21 cm", "https://upload.wikimedia.org/wikipedia/commons/3/31/Johannes_Vermeer_-_The_Lacemaker_-_WGA24689.jpg", 4),
("The Milkmaid", "Johannes Vermeer", "vers 1657-1658", "peinture", "45,5 x 41 cm", "https://upload.wikimedia.org/wikipedia/commons/4/4e/Vermeer_The_Milkmaid_1660_ca.jpg", 4),
("Woman with a Balance", "Johannes Vermeer", "vers 1663-1664", "peinture", "42,5 x 38 cm", "https://upload.wikimedia.org/wikipedia/commons/6/68/Johannes_Vermeer_-_Woman_Holding_a_Balance_-_Google_Art_Project.jpg", 4),
("Woman with a Pearl Necklace", "Johannes Vermeer", "vers 1664", "peinture", "55 x 45 cm", "https://upload.wikimedia.org/wikipedia/commons/7/7e/Johannes_Vermeer_-_Woman_with_a_Pearl_Necklace_-_WGA24659.jpg", 4),
("Young Girl with a Flute", "Johannes Vermeer", "vers 1655-1660", "peinture", "20 x 17,8 cm", "https://upload.wikimedia.org/wikipedia/commons/7/7e/Johannes_Vermeer_-_Girl_with_a_flute_%28c_1665-1670%29.jpg", 4),
("The Little Street in Delft", "Johannes Vermeer", "vers 1658-1660", "peinture", "54,3 x 44 cm", "https://upload.wikimedia.org/wikipedia/commons/2/2b/Johannes_Vermeer_-_Gezicht_op_huizen_in_Delft%2C_bekend_als_%27Het_straatje%27_-_Google_Art_Project.jpg", 4),
("A Young Woman Seated at the Virginals", "Johannes Vermeer", "vers 1670-1672", "peinture", "25 x 20 cm", "https://upload.wikimedia.org/wikipedia/commons/2/2b/Vermeer_-_A_young_Woman_seated_at_the_Virginals.jpg", 4);
