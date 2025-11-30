import os
import shutil 
import sys

def demo_cwd():
    print(f"--- ΕΠΙΔΕΙΞΗ 0a: CWD ---")
    
    current_dir = os.getcwd()
    print(f"1. Ο τρέχων κατάλογος μου (CWD) είναι: {current_dir}")

    try:
        os.chdir("non_existent_directory")
    except FileNotFoundError as e:
        print(f"2. Σφάλμα (αναμενόμενο) κατά την αλλαγή καταλόγου: {e}")
        print(f"   Παραμένω στο: {os.getcwd()}")

def demo_path_join():
    print(f"\n--- ΕΠΙΔΕΙΞΗ 0b: os.path ---")
    
    dir_name = "data_files"
    file_name = "report.txt"
    portable_path = os.path.join(dir_name, file_name)

    print(f"1. Η διαδρομή που δημιουργήθηκε (φορητά): {portable_path}")

    full_path_example = os.path.join("home", "user", "project", "main.py")
    print(f"\n2. --- Ανάλυση Διαδρομής ---")
    print(f"   Πλήρης Διαδρομή: {full_path_example}")
    print(f"   Dirname (Κατάλογος): {os.path.dirname(full_path_example)}")
    print(f"   Basename (Όνομα): {os.path.basename(full_path_example)}")
    print(f"   Absolute Path (π.χ. του CWD): {os.path.abspath('.')}")

def demo_scandir(target_dir="."):
    print(f"\n--- ΕΠΙΔΕΙΞΗ 1: Σάρωση Καταλόγου '{target_dir}' ---")
    
    if not os.path.exists(target_dir):
        print(f"Σφάλμα: Ο κατάλογος '{target_dir}' δεν υπάρχει.")
        return

    if not os.path.isdir(target_dir):
        print(f"Σφάλμα: Το '{target_dir}' είναι αρχείο, όχι κατάλογος.")
        return
        
    print(f"Περιεχόμενα του '{os.path.abspath(target_dir)}':")
    try:
        items = os.listdir(target_dir)
        
        if not items:
            print(" (Ο κατάλογος είναι άδειος)")
            return
            
        for item_name in items:
            item_path = os.path.join(target_dir, item_name)
            
            if os.path.isdir(item_path):
                print(f"  [Κατάλογος] {item_name}")
            elif os.path.isfile(item_path):
                print(f"  [Αρχείο]     {item_name}")
            else:
                print(f"  [Άλλο]       {item_name} (π.χ. symbolic link)")

    except PermissionError:
        print(f"Σφάλμα: Δεν έχω δικαίωμα πρόσβασης στον κατάλογο '{target_dir}'.")
    except Exception as e:
        print(f"Προέκυψε ένα μη αναμενόμενο σφάλμα: {e}")

def demo_create_modify_delete(base_dir="demo_test_area"):
    print(f"\n--- ΕΠΙΔΕΙΞΗ 2: Τροποποίηση Συστήματος Αρχείων ---")
    
    if os.path.exists(base_dir):
        print(f"Ο '{base_dir}' υπάρχει ήδη. Γίνεται αναγκαστικός καθαρισμός...")
        try:
            shutil.rmtree(base_dir) 
        except OSError as e:
            print(f"Σφάλμα καθαρισμού: {e}")
            return
    
    print(f"1. Δημιουργία '{base_dir}' με os.mkdir()")
    try:
        os.mkdir(base_dir)
    except OSError as e:
        print(f"   Σφάλμα: {e}")
        return 

    nested_path = os.path.join(base_dir, "nested", "data")
    print(f"\n2. Δημιουργία '{nested_path}' με os.makedirs()")
    os.makedirs(nested_path, exist_ok=True)
    
    file_path = os.path.join(nested_path, "file_to_move.txt")
    print(f"3. Δημιουργία αρχείου: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("test content")
    except IOError as e:
        print(f"   Σφάλμα δημιουργίας αρχείου: {e}")
        
    new_path = os.path.join(base_dir, "MOVED_file.txt")
    print(f"\n4. Μετακίνηση '{file_path}' -> '{new_path}'")
    try:
        os.rename(file_path, new_path)
    except OSError as e:
        print(f"   Σφάλμα μετακίνησης: {e}")

    print(f"\n5. Διαγραφή αρχείου: {new_path}")
    try:
        os.remove(new_path)
    except OSError as e:
        print(f"   Σφάλμα διαγραφής: {e}")

    print(f"\n6. Διαγραφή άδειου καταλόγου: {nested_path}")
    try:
        os.rmdir(nested_path) 
    except OSError as e:
        print(f"   Σφάλμα διαγραφής (μήπως δεν είναι άδειος;): {e}")

    print(f"\n7. Προσπάθεια διαγραφής ΜΗ-ΑΔΕΙΟΥ καταλόγου: {base_dir}")
    try:
        os.rmdir(base_dir)
    except OSError as e:
        print(f"   Σφάλμα (αναμενόμενο): {e}")
        print(f"   (Ο κατάλογος '{base_dir}' δεν είναι άδειος)")
    
    print(f"\n8. Τελικός καθαρισμός του '{base_dir}' με shutil.rmtree()")
    try:
        shutil.rmtree(base_dir)
        print("   Καθαρισμός ΟΚ.")
    except OSError as e:
        print(f"   Σφάλμα τελικού καθαρισμού: {e}")

def demo_full_setup_teardown(demo_dir="FINAL_DEMO"):
    print(f"\n--- ΕΠΙΔΕΙΞΗ 3: Ολοκληρωμένο Σενάριο (Setup/Teardown) ---")
    print(f"Θα χρησιμοποιηθεί ο κατάλογος: {demo_dir}\n")

    if os.path.exists(demo_dir):
        print(f"[Setup] Ο '{demo_dir}' βρέθηκε. Γίνεται καθαρισμός...")
        try:
            shutil.rmtree(demo_dir)
            print("[Setup] Καθαρισμός επιτυχής.")
        except OSError as e:
            print(f"[Setup] Σφάλμα κατά τον καθαρισμό: {e}")
            return 

    try:
        print(f"\n[Try] Εκτέλεση κύριας λογικής...")
        
        print(f"[Try] Δημιουργία ιεραρχίας 'reports/2023'...")
        reports_dir = os.path.join(demo_dir, "reports", "2023")
        os.makedirs(reports_dir)
        
        print(f"[Try] Δημιουργία αρχείων report...")
        with open(os.path.join(reports_dir, "report_01.txt"), 'w') as f:
            f.write("Data 1")
        with open(os.path.join(reports_dir, "report_02.txt"), 'w') as f:
            f.write("Data 2")

        print(f"[Try] Δημιουργία ιεραρχίας 'logs'...")
        logs_dir = os.path.join(demo_dir, "logs")
        os.makedirs(logs_dir)
        with open(os.path.join(logs_dir, "app.log"), 'w') as f:
            f.write("App started\n")

        print(f"[Try] Η λογική εκτελέστηκε επιτυχώς.")
        
    except (OSError, IOError) as e:
        print(f"\n[Except] ΣΟΒΑΡΟ ΣΦΑΛΜΑ κατά την επεξεργασία: {e}")
    except ValueError as e:
        print(f"\n[Except] ΣΦΑΛΜΑ ΛΟΓΙΚΗΣ: {e}")

    finally:
        print(f"\n[Finally] Εκτέλεση φάσης τελικού καθαρισμού...")
        if os.path.exists(demo_dir):
            print(f"[Finally] Διαγραφή '{demo_dir}' (shutil.rmtree)...")
            try:
                shutil.rmtree(demo_dir)
                print(f"[Finally] Καθαρισμός ΟΚ.")
            except OSError as e:
                print(f"[Finally] Σφάλμα στον τελικό καθαρισμό: {e}")
        else:
            print("[Finally] Ο κατάλογος δεν δημιουργήθηκε, δεν απαιτείται καθαρισμός.")

    print("\n--- Τέλος Επίδειξης 3 ---")


if __name__ == "__main__":
    print("=================================================")
    print("   Εκτέλεση ΣΕΝΑΡΙΩΝ ΕΠΙΔΕΙΞΗΣ 'os' module")
    print("=================================================\n")
    
    demo_cwd()
    demo_path_join()
    demo_scandir() 
    demo_create_modify_delete(base_dir="temp_demo_area_1")
    demo_full_setup_teardown(demo_dir="temp_demo_area_2")
    
    print("\n=================================================")
    print("   Η εκτέλεση όλων των σεναρίων ολοκληρώθηκε.")
    print("=================================================")