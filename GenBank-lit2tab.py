from Bio import SeqIO
import re

filename = str(input("Insert GenBank filename: "))
print("\nOpening file...")
handle = open(filename, "rU")
print("File opened!\n")
output_filename = str(input("Insert output filename: "))
output = open(output_filename, "w")
print("Parsing file...")
seq_list = list(SeqIO.parse(handle, "genbank"))
handle.close()
print("File parsed!\n")

head = ["Title", "Authors", "Journal", "PMID"]
header = str("$".join(head)) + "\n"

init_list = []
print("Collecting information...")
direct_sub = 0
unpublished = 0
old_articles = 0
rejected_articles = 0
n_accessions = 0
for i in range(0, len(seq_list)):
	annotation = seq_list[i].annotations
	n_accessions += 1

	try:
		comment = str(annotation["comment"]).replace("\n"," ")
	except KeyError:
		comment = "N/A"
	try:	
		ref = seq_list[i].annotations["references"]
		for j in range(0, len(ref)):
			authors_ = ref[j].authors
			ttl = ref[j].title
			pubmedid = ref[j].pubmed_id
			jrnl = ref[j].journal

			if authors_ == "":
				authors_ = "N/A"
				
			if ttl == "":
				ttl = "N/A"
			if ttl.lower() == "direct submission":
				direct_sub +=1
				continue

			if jrnl == "":
				jrnl = "N/A"
			elif jrnl == "Unpublished":
				unpublished += 1
				continue
				
			if pubmedid == "":
				pubmedid = "N/A"

			year_match = re.search('[1][9][0-9][0-9]|[2][0][01][0-8]', jrnl)
			if year_match:
				year = year_match.group()
				if int(year) < 2012:
					old_articles += 1
					continue
			else:
				rejected_articles += 1
				continue

			list = [ttl, authors_, jrnl, year, pubmedid]
			line = str("$".join(list))+"\n"
			init_list.append(line)
			
	except KeyError:
		pass
	
print("Information collected!\n")

del seq_list

print("Removing duplicates...")

final_list = []
for ref in init_list:
	if ref not in final_list:
		final_list.append(ref)

print("Duplicates Removed!\n")

print("Writing output...")

output.write("Direct_subm$Unpublished$Old_articles$NoYearInfo$No.SequencesinGBfile\n")
direct_unpub = str(direct_sub) + "$" + str(unpublished) + "$" + str(old_articles) + "$" + str(rejected_articles) + "$" + str(n_accessions) + "\n\n"
output.write(direct_unpub)
output.write("Title$Authors$Journal$Year$PMID\n")
for i in range(0,len(final_list)):
	line = final_list[i]
	output.write(line)
print("Output Saved!")	

print("Output saved as: " + output_filename)
print("\n")
