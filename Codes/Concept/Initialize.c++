#include <iostream>
using namespace std;

// Structure definition
struct Student {
    char name[50];
    int id;
    int fee;
};

int i = 0, d = 0;
int de[10];

// Function for adding info
Student addInfo() {
    Student sa;
    // Input
    cout << "Student " << i << ":" << endl;
    cout << "Name: ";
    cin >> sa.name;
    cout << "ID: ";
    cin >> sa.id;
    cout << "Fee: ";
    cin >> sa.fee;
    i++;
    return sa;
}

// Function for updating
Student update(int x) {
    Student sa;
    // Input
    cout << "Student " << x << ":" << endl;
    cout << "Name: ";
    cin >> sa.name;
    cout << "ID: ";
    cin >> sa.id;
    cout << "Fee: ";
    cin >> sa.fee;
    return sa;
}

int main() {
    // Array of structure
    Student s[10];
    next:
    cout << "1 For addInfo" << endl;
    cout << "2 For update" << endl;
    cout << "3 For delete" << endl;
    cout << "4 For Exit" << endl;
    int n;
    cin >> n;
    switch (n) {
        case 1: {
            s[i] = addInfo();
            goto next;
        }
        case 2: {
            int x;
            cout << "Student NO.:" << endl;
            cin >> x;
            s[x] = update(x);
            goto next;
        }
        case 3: {
            cout << "Student No." << endl;
            int x;
            cin >> x;
            de[d] = x;
            d++;
            goto next;
        }
        case 4: {
            int j;
            for (j = 0; j < i; j++) {
                int x;
                for (x = 0; x < d; x++) {
                    if (j == de[x])
                        cout << "INFO IS DELETED" << endl;
                    else {
                        cout << "Student " << j << endl;
                        cout << "Name: " << s[j].name << endl;
                        cout << "ID: " << s[j].id << endl;
                        cout << "Fee: " << s[j].fee << endl;
                    }
                }
            }
        }
    }
    return 0;
}
