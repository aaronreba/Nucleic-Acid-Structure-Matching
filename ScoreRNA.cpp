#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <utility>
#include <stdint.h>
#include <stack>
#include <string>
#include <unistd.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <sstream>

using namespace std;

/*
arguments:
$1: target representation file created in ScoreRNA.py
$2: file with test sequences and their folds
$3: file which will hold scoring information
*/
//using vectors in place of stacks because the stack class is quite limiting

string make_realistic_fold(string subfold){
	//removes invalid () in a string like so:
	//given: ...)...()...(...
	//gives: .......().......
	string real_fold;
	vector <int32_t> real_fold_stack;
	vector <int32_t> make_periods;
	
	real_fold = subfold;
	
	for ( int32_t i = 0; i < subfold.size(); i++ ){
		if (subfold[i] == '(' ||
				subfold[i] == '<'){
			real_fold_stack.push_back (i);
		}
		else if (subfold[i] == ')' ||
						 subfold[i] == '>'){
			if ( real_fold_stack.size() > 0){
				real_fold_stack.pop_back();
			}
			else{
				make_periods.push_back( i );
			}
		}
	}
	
	for ( int32_t i = 0; i < real_fold_stack.size(); i++ ){
		real_fold.replace ( real_fold_stack[i], 1, 1, '.' );
	}
	
	for ( int32_t i = 0; i < make_periods.size(); i++ ){
		real_fold.replace ( make_periods[i], 1, 1, '.' );
	}
	
	return real_fold;
}

int32_t score_sequence(string subtarget,
                       string subsequence){
	//scores a sequence of characters to a target
	//2 points for each matching base
	//1 if target is Y and sequence is U or C
	//1 if target is R and sequence is A or G
	int32_t score = 0;
	int32_t i = 0;
	while (1){
		if (subtarget[i] == subsequence[i]){
			score += 2;
		}
		else if ( subtarget[i] == 'Y' ) {
			if ( subsequence[i] == 'U' || subsequence[i] == 'C' ){
				score += 1;
			}
		}
		else if ( subtarget[i] == 'R' ) {
			if ( subsequence[i] == 'A' || subsequence[i] == 'G' ){
				score += 1;
			}
		}
		i++;
		if (subtarget[i] == '\0'){
			return score;
		}
	}
}

int32_t get_max_score(string subentry){
	//this is never called
	int32_t score;
	
	score = 0;
	
	for (int32_t i = 0; i < subentry.size(); i ++){
		if ( subentry[i] == '(' || subentry[i] == '<' ){
			score++;
		}
	}
	return score << 1;
}

int32_t score_fold(string subtarget,
                   string subfold){
	//scores a fold to a target
	//given:
	//fold:   (((...)))
	//target: <<.....>>
	//returns 4
	vector<pair<int32_t, int32_t> > fold_stack;
	vector<pair<int32_t, int32_t> > target_stack;
	
	int32_t fold_stack_size;
	int32_t target_stack_size;
	
	pair<int32_t, int32_t> fold_entry;	
	pair<int32_t, int32_t> target_entry;
	
	pair<int32_t, int32_t> last_fold_entry;	
	pair<int32_t, int32_t> last_target_entry;
	
	last_target_entry.first = -1;
	last_target_entry.second = -1;
	last_fold_entry.first = -1;
	last_fold_entry.second = -1;
	
	int32_t subtarget_size;
	int32_t current_score;
	
	fold_stack_size = 0;
	target_stack_size = 0;
	
	subtarget_size = subtarget.size();
	current_score = 0;
	
	bool valid_fold;
	
	for (int32_t i = 0; i < subtarget_size; i++){
		if (subfold[i] == '('){
			fold_entry.first = i;
			fold_entry.second = fold_stack.size();
			fold_stack.push_back(fold_entry);
			fold_stack_size++;
		}
		
		if ( subtarget[i] == '<' ){
			target_entry.first = i;
			target_entry.second = target_stack.size();
			target_stack.push_back(target_entry);
			target_stack_size++;
		}
		
		if ( subfold[i] == ')' ){
			if (fold_stack_size > 0){
				last_fold_entry = fold_stack.back();
				fold_stack.pop_back();
				fold_stack_size--;
				valid_fold = true;
			}
			else{
				valid_fold = false;
			}
		}
		
		if ( subtarget[i] == '>' ){
			last_target_entry = target_stack.back();
			target_stack.pop_back();
			target_stack_size--;
			if (subfold[i] == ')' && valid_fold){
				if (last_target_entry.first == last_fold_entry.first &&
						last_target_entry.second == target_stack_size &&
						last_fold_entry.second == fold_stack_size){
					current_score += 1;
				}
			}
		}
	}
	
	return current_score;
}

void update_fold_score_map(string subfold,
                           int32_t index,
                           int32_t subfold_score,
                           std::map<string, int32_t> &fold_scores){
  for(std::map<string, int32_t>::iterator i = fold_scores.begin();
      i != fold_scores.end();
      i ++){
    string current_substring;
    string fold;
    fold = (*i).first;
    current_substring = fold.substr(index, subfold.size());
    
    if (current_substring == subfold){
      if (fold_scores[fold] < subfold_score){
        fold_scores[fold] = subfold_score;
      }
    }
  }
}

struct subfold_entry {
	string subfold;
	int32_t index;
};

struct subtarget_entry {
  string name;
  string subtarget;
  int32_t index;
};

struct target_entry {
  string name;
  string target;
};

int main(int argc, char* argv[]){
  string target;
  string target_name;
  string best_target;
  string best_target_name;
  int32_t best_target_index;
  string subtarget;
  
  target_entry using_target;
  vector < target_entry > targets;
  
  int32_t subtarget_index;
  subtarget_entry using_subtarget;
  vector < subtarget_entry > using_subtargets;
  
  string sequence_name;
  string sequence;
  string subsequence;
  int32_t subsequence_index;
  pair <string, int32_t> using_subsequence;
  vector < pair<string, int32_t> > using_subsequences;
  
  string fold;
  string last_fold;
  map <string, char> all_folds;
  
  string best_fold;
  string subfold;
  string real_fold;
  int32_t subfold_index;
  int32_t best_subfold_index;
  
  subfold_entry using_subfold;
  vector < subfold_entry > using_subfolds;
  
  int32_t number_of_alignments;
  
  pair <string, string> scored_fold_entry;
  map < pair <string, string>, int32_t> scored_folds;
  
  int32_t possible_max_score;
  int32_t sequence_score;
  int32_t fold_score;
  int32_t best_sequence_score;
  int32_t best_fold_score;
  int32_t best_score;
  pair<string, double> chronological_fold;
  vector< pair<string, double> > chronological_folds;
  map<string, int32_t> full_fold_scores;
  
  string target_file_name;
  string test_file_name;
  string score_file_name;
  
  ifstream target_file;
  ifstream test_file;
  ofstream score_file;
  
  //DIR *chronological_dp;
  //struct dirent *dirp;
  
  long seconds;
  long useconds;
  long create_test_time;
  long score_time = 0;
  long func_time;
  timeval start;
  timeval end;
  timeval score_start;
  timeval score_end;
  
  bool enable_chronology;
  enable_chronology = false;
  string chrono_directory;
  
  bool enable_fold_score;
  enable_fold_score = false;
  string fold_directory;
  
  int fold_threshold;
  bool enable_fold_threshold;
  enable_fold_threshold = false;
  
  if (argc >= 5){
    for (int32_t i = 4; i < argc; i++){
      if (string(argv[i]) == "chrono"){
        chrono_directory = argv[i + 1];
        string call_mkdir = "mkdir " + chrono_directory;
        system( call_mkdir.c_str() );
        enable_chronology = true;
        i++;
      }
      
      else if (string(argv[i]) == "rawfold"){
        fold_directory = argv[i + 1];
        string call_mkdir = "mkdir " + fold_directory;
        system( call_mkdir.c_str() );
        enable_fold_score = true;
        i++;
      }
      
      else if (string(argv[i]) == "threshold"){
        enable_fold_threshold = true;
        string temp;
        temp = argv[i + 1];
        istringstream (temp.c_str()) >> fold_threshold;
        i++;
      }
    }
    
  }
  int looking, not_looking;
  looking = 0;
  not_looking = 0;
  
  target_file_name = argv[1];
  test_file_name = argv[2];
  score_file_name = argv[3];
  
  create_test_time = 0;
  score_time = 0;
  func_time = 0;
  
  target_file.open ( target_file_name.c_str() );
  test_file.open ( test_file_name.c_str() );
  score_file.open ( score_file_name.c_str() );
  
  //store all targets in the target vector named targets
  while ( target_file >> target_name >> target ){
    using_target.name = target_name;
    using_target.target = target;
    
    targets.push_back ( using_target );
  }
  
  //skipping '>'
  test_file >> sequence_name;
  
  //first line to examine is sequence name line
  
  while ( test_file >> sequence_name ){
    double last_fold_time;
    
    //reading into sequence_name twice because of > character
    test_file >> sequence;
    
    all_folds.clear();
    scored_folds.clear();
    chronological_folds.clear();
    full_fold_scores.clear();
    
    last_fold_time = -1;
    
    while ( test_file >> fold){
      double fold_energy;
      double fold_time;
      
      //read and score folds until a '>' is reached
      if ( fold == ">" ){
        fold = last_fold;
        break;
      }
      
      test_file >> fold_energy >> fold_time;
      
      if (fold_time < last_fold_time){
        chronological_fold.first = fold;
        chronological_fold.second = 0;
        chronological_folds.push_back(chronological_fold);
      }
      
      chronological_fold.first = fold;
      chronological_fold.second = fold_time;
      chronological_folds.push_back(chronological_fold);
      if (all_folds.count(fold) == 0){
        if (enable_fold_threshold){
          if (fold_threshold <= std::count(fold.begin(), fold.end(), '(')){
            all_folds[fold] = '.';
            full_fold_scores[fold] = 0;
          }
        }
        else{
          all_folds[fold] = '.';
          full_fold_scores[fold] = 0;
        }
      }
      last_fold = fold;
      last_fold_time = fold_time;
    }
    
    //compare the folds to each possible template
    
    best_score = -1;
    
    //first, make all comparisons of all targets and the folds
    
    for ( int32_t i = 0; i < targets.size(); i++ ){
      
      target_name = targets[i].name;
      target = targets[i].target;
      
      //if the target is longer than the sequence, substrings of the target
      //will have to be used when comparing
      //otherwise, substrings of the sequence and fold will be used.
      number_of_alignments = abs(int(target.size() - fold.size())) + 1;
      
      for ( int32_t j = 0; j < number_of_alignments; j++){
        using_subtargets.clear();
        using_subsequences.clear();
        using_subfolds.clear();
        
        //if target is bigger, make substrings of target
        if ( target.size() > fold.size() ){
          using_subtarget.name = target_name;
          using_subtarget.subtarget = target.substr ( j, sequence.size() );
          using_subtarget.index = j;
          using_subtargets.push_back ( using_subtarget );
          
          using_subsequence.first = sequence;
          using_subsequence.second = 0;
          using_subsequences.push_back ( using_subsequence );
          
          using_subfold.subfold = fold;
          using_subfold.index = 0;
          
          using_subfolds.push_back ( using_subfold );
        }
        
        // if sequence/folds are bigger, make substrings of sequence/folds
        else if ( target.size() < fold.size() ){
          using_subtarget.name = target_name;
          
          using_subtarget.subtarget = target;
          using_subtarget.index = 0;
          using_subtargets.push_back ( using_subtarget );
          
          using_subsequence.first = sequence.substr ( j, target.size() );
          using_subsequence.second = j;
          using_subsequences.push_back ( using_subsequence );
          
          for(map <string, char>::iterator k = all_folds.begin();
              k != all_folds.end();
              k ++){
            subfold = (*k).first.substr ( j, target.size() );
            using_subfold.subfold = subfold;
            using_subfold.index = j;
            
            using_subfolds.push_back ( using_subfold );
          }
            
        }
        
        //they're equal length, no need to make substrings of target, sequence,
        //or folds
        else{
          using_subtarget.name = target_name;
          using_subtarget.subtarget = target;
          using_subtarget.index = 0;
          using_subtargets.push_back ( using_subtarget );
          
          using_subsequence.first = sequence;
          using_subsequence.second = 0;
          using_subsequences.push_back ( using_subsequence );
          
          using_subfold.subfold = fold;
          using_subfold.index = 0;
          using_subfolds.push_back ( using_subfold );
        }
        
        //gettimeofday (&start, NULL);
        for ( int32_t k = 0; k < using_subtargets.size(); k++ ){
          
          
          subtarget_index = using_subtargets[k].index;
          subtarget = using_subtargets[k].subtarget;
          target_name = using_subtargets[k].name;
          
          for ( int32_t l = 0; l < using_subsequences.size(); l++ ){
            //using_subsequence = using_subsequences[j];
            
            
            subsequence = using_subsequences[l].first;
            subsequence_index = using_subsequences[l].second;
            
            sequence_score = score_sequence(subtarget, subsequence);
            
            best_fold_score = -1;
            
            for ( int32_t m = 0; m < using_subfolds.size(); m++ ){
              //using_subfold = using_subfolds[l];
              
              subfold = using_subfolds[m].subfold;
              subfold_index = using_subfolds[m].index;
              
              //make subfold into a realistic fold
              
              //real_fold = make_realistic_fold(subfold);
              
              //check if the fold is in the scored_folds map
              //if it is, use that score
              //else, find the score of the fold
              scored_fold_entry.first = subfold;
              scored_fold_entry.second = subtarget;
              
              if (fold_threshold > std::count(subfold.begin(), subfold.end(), '(') ||
                  fold_threshold > std::count(subfold.begin(), subfold.end(), ')')){
                fold_score = 0;
              }
              else if ( scored_folds.count( scored_fold_entry ) > 0 ){
                fold_score = scored_folds[ scored_fold_entry ];
              }
              else {
                
                fold_score = score_fold(subtarget, subfold);
                
                scored_folds[scored_fold_entry] = fold_score;
                //update chronological_folds and all_fold_scores
                update_fold_score_map(subfold,
                                      subsequence_index,
                                      fold_score,
                                      full_fold_scores);
              }
              
              
              
              //checking best
              if ( fold_score + sequence_score > best_score ) {
                best_score = fold_score + sequence_score;
                best_fold = subfold;
                best_fold_score = fold_score;
                best_subfold_index = subfold_index;
                best_target = subtarget;
                best_target_name = target_name;
                best_target_index = subtarget_index;
              }
            }
          }
        }
//      gettimeofday (&end, NULL);
      
//      seconds  = end.tv_sec  - start.tv_sec;
//      useconds = end.tv_usec - start.tv_usec;
  
//      score_time += ((seconds) * 1000 + useconds/1000.0) + 0.5;
      }
    }
    
    score_file << "> " << sequence_name << " scored with the template sequence "
               << best_target_name << endl;
    score_file << "score: " << best_score << endl;
    score_file << string(best_target_index, ' ') << sequence << endl;
    
    for(map <string, char>::iterator i = all_folds.begin();
      i != all_folds.end();
      i ++){
      
      if ( best_fold == (*i).first.substr( best_subfold_index, best_target.size() ) ){
        best_fold = (*i).first;
        break;
      }
    }
    
    score_file << string(best_target_index, ' ') << best_fold << endl;
    
    for (int32_t i = 0; i < targets.size(); i++){
      if ( best_target ==  targets[i].target.substr( best_target_index, best_target.size() ) ){
        best_target = targets[i].target;
      }
    }
    
    score_file << string(best_subfold_index, ' ') << best_target << endl;
    score_file.flush();
    
    if (enable_chronology){
      ofstream chronological_file;
      string chronological_file_name;
      
      chronological_file_name = chrono_directory + "//chrono" + sequence_name + ".txt";
      chronological_file.open(chronological_file_name.c_str());
      
      int32_t previous_score;
      double previous_time;
      
      previous_time = -1;
      previous_score = 0;
      
      chronological_file << 0 << "\t" << 0 << endl;
      
      for (int32_t i = 0; i < chronological_folds.size(); i++){
        int32_t current_score;
        
        chronological_fold = chronological_folds[i];
        
        if (chronological_fold.second < previous_time){
          chronological_file << 0 << "\t" << 0 << endl;
          previous_score = 0;
          previous_time = chronological_fold.second;
          continue;
        }
        previous_time = chronological_fold.second;
        
        
        current_score = full_fold_scores[chronological_fold.first];
        
        
        if (current_score > previous_score){
          previous_score = current_score;
          chronological_file << chronological_fold.second << "\t" 
                             << current_score << endl;
        }
        
      }
      chronological_file.close();
    }
    
    if (enable_fold_score){
      ofstream fold_file;
      string fold_file_name;
      
      fold_file_name = fold_directory + "//fold" + sequence_name + ".txt";
      fold_file.open(fold_file_name.c_str());
      
      double previous_time;
      int32_t previous_score;
      
      previous_time = -1;
      previous_score = 0;
      
      for (int32_t i = 0; i < chronological_folds.size(); i++){
        int32_t current_score;
        
        chronological_fold = chronological_folds[i];
        
        if (chronological_fold.second < previous_time){
          fold_file << previous_score << endl;
          previous_score = -1;
        }
        
        previous_time = chronological_fold.second;
        if (full_fold_scores.count(chronological_fold.first) == 0){
          current_score = 0;
        }
        else{
          current_score = full_fold_scores[chronological_fold.first];
        }
        
        if (current_score > previous_score){
          previous_score = current_score;
        }
        
      }
      
      fold_file << previous_score << endl;
      
      fold_file.close();
    }
    
  }
  //cout << score_time << endl;
  score_file.close();
  target_file.close();
  test_file.close();
  
  
  return 0;
}
