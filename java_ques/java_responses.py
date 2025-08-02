# java_ques/java_responses.py
import re
java_answers = {

    "factorial": """
public class Main {
    public static void main(String[] args) {
        int n = 5, fact = 1;
        for (int i = 1; i <= n; i++) {
            fact *= i;
        }
        System.out.println("Factorial: " + fact);
    }
}
""",

    "palindrome": """
public class Main {
    public static void main(String[] args) {
        String str = "madam", rev = "";
        for (int i = str.length()-1; i >= 0; i--)
            rev += str.charAt(i);
        System.out.println(str.equals(rev) ? "Palindrome" : "Not a palindrome");
    }
}
""",

    "fibonacci": """
public class Main {
    public static void main(String[] args) {
        int n = 10, a = 0, b = 1;
        for (int i = 1; i <= n; i++) {
            System.out.print(a + " ");
            int sum = a + b;
            a = b;
            b = sum;
        }
    }
}
""",

    "reverse string": """
public class Main {
    public static void main(String[] args) {
        String input = "hello";
        String reversed = "";
        for (int i = input.length() - 1; i >= 0; i--)
            reversed += input.charAt(i);
        System.out.println("Reversed: " + reversed);
    }
}
""",

    "count digits": """
public class Main {
    static int countDigits(int n) {
        if (n == 0) return 0;
        return 1 + countDigits(n / 10);
    }
    public static void main(String[] args) {
        System.out.println("Digit count: " + countDigits(123456));
    }
}
""",

    "print 1 to n": """
public class Main {
    static void printAsc(int n) {
        if (n == 0) return;
        printAsc(n - 1);
        System.out.print(n + " ");
    }
    public static void main(String[] args) {
        printAsc(5);
    }
}
""",

    "print n to 1": """
public class Main {
    static void printDesc(int n) {
        if (n == 0) return;
        System.out.print(n + " ");
        printDesc(n - 1);
    }
    public static void main(String[] args) {
        printDesc(5);
    }
}
""",

    "check array sorted": """
public class Main {
    static boolean isSorted(int[] arr, int i) {
        if (i == arr.length - 1) return true;
        if (arr[i] > arr[i + 1]) return false;
        return isSorted(arr, i + 1);
    }
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 5, 7};
        System.out.println("Is sorted? " + isSorted(arr, 0));
    }
}
""",

    "prime number": """
public class Main {
    public static void main(String[] args) {
        int n = 29, count = 0;
        for (int i = 2; i <= n/2; i++) {
            if (n % i == 0) {
                count++;
                break;
            }
        }
        System.out.println(count == 0 ? "Prime" : "Not Prime");
    }
}
""",

    "armstrong number": """
public class Main {
    public static void main(String[] args) {
        int n = 153, temp = n, sum = 0;
        while (temp != 0) {
            int remainder = temp % 10;
            sum += remainder * remainder * remainder;
            temp /= 10;
        }
        System.out.println(sum == n ? "Armstrong" : "Not Armstrong");
    }
}
""",

    "sum of digits": """
public class Main {
    public static void main(String[] args) {
        int n = 1234, sum = 0;
        while (n != 0) {
            sum += n % 10;
            n /= 10;
        }
        System.out.println("Sum of digits: " + sum);
    }
}
""",

    "swap numbers": """
public class Main {
    public static void main(String[] args) {
        int a = 5, b = 10;
        a = a + b;
        b = a - b;
        a = a - b;
        System.out.println("a = " + a + ", b = " + b);
    }
}
""",

    "largest of three": """
public class Main {
    public static void main(String[] args) {
        int a = 20, b = 25, c = 22;
        if (a >= b && a >= c)
            System.out.println("Largest: " + a);
        else if (b >= c)
            System.out.println("Largest: " + b);
        else
            System.out.println("Largest: " + c);
    }
}
""",

    "leap year": """
public class Main {
    public static void main(String[] args) {
        int year = 2024;
        boolean isLeap = (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
        System.out.println(isLeap ? "Leap Year" : "Not Leap Year");
    }
}
""",

    "linear search": """
public class Main {
    public static void main(String[] args) {
        int[] arr = {4, 2, 7, 1, 9};
        int key = 7;
        boolean found = false;
        for (int n : arr) {
            if (n == key) {
                found = true;
                break;
            }
        }
        System.out.println(found ? "Found" : "Not Found");
    }
}
""",

    "binary search": """
public class BinarySearchExample {

    // This method performs binary search on a sorted array
    public static int binarySearch(int[] arr, int target) {
        int low = 0;                        // First index
        int high = arr.length - 1;         // Last index

        while (low <= high) {
            int mid = (low + high) / 2;    // Find the middle index

            if (arr[mid] == target) {
                return mid;                // Target found at index 'mid'
            } else if (arr[mid] < target) {
                low = mid + 1;             // Ignore left half
            } else {
                high = mid - 1;            // Ignore right half
            }
        }

        return -1;                         // Target not found
    }

    // Main method to test the binary search
    public static void main(String[] args) {
        int[] numbers = {4, 7, 10, 12, 18, 22, 27, 31, 39};  // Must be sorted
        int target = 22;                                     // Value to find

        int result = binarySearch(numbers, target);          // Perform search

        if (result == -1) {
            System.out.println("Element not found.");
        } else {
            System.out.println("Element found at index: " + result);
        }
    }
}
""",

    "reverse number": """
public class Main {
    public static void main(String[] args) {
        int num = 1234, rev = 0;
        while (num != 0) {
            rev = rev * 10 + (num % 10);
            num /= 10;
        }
        System.out.println("Reversed: " + rev);
    }
}
""",

    "sum of array": """
public class Main {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4};
        int sum = 0;
        for (int n : arr)
            sum += n;
        System.out.println("Sum: " + sum);
    }
}
""",

    "find duplicate elements": """
import java.util.HashSet;
public class Main {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 2, 4, 1};
        HashSet<Integer> seen = new HashSet<>();
        for (int n : arr) {
            if (!seen.add(n))
                System.out.println("Duplicate: " + n);
        }
    }
}
""",

    "sum of n natural numbers": """
public class Main {
    public static void main(String[] args) {
        int n = 10;
        int sum = n * (n + 1) / 2;
        System.out.println("Sum: " + sum);
    }
}
""",

    "palindrome number": """
public class Main {
    public static void main(String[] args) {
        int num = 121, rev = 0, temp = num;
        while (temp != 0) {
            int remainder = temp % 10;
            rev = rev * 10 + remainder;
            temp /= 10;
        }
        System.out.println(num == rev ? "Palindrome" : "Not Palindrome");
    }
}
""",

    "armstrong 4 digit": """
public class Main {
    public static void main(String[] args) {
        for (int num = 1000; num <= 9999; num++) {
            int temp = num, sum = 0;
            while (temp != 0) {
                int d = temp % 10;
                sum += Math.pow(d, 4);
                temp /= 10;
            }
            if (sum == num)
                System.out.println(num);
        }
    }
}
""",

    "print ascii values": """
public class Main {
    public static void main(String[] args) {
        for (char c = 'A'; c <= 'Z'; c++) {
            System.out.println(c + " = " + (int)c);
        }
    }
}
""",

    "bubble_sort": """
public class BubbleSort {
    public static void main(String[] args) {
        int[] arr = {5, 1, 4, 2, 8};
        for (int i = 0; i < arr.length - 1; i++)
            for (int j = 0; j < arr.length - i - 1; j++)
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }

        for (int num : arr)
            System.out.print(num + " ");
    }
}
""",

    "selection_sort": """
public class SelectionSort {
    public static void main(String[] args) {
        int[] arr = {29, 10, 14, 37, 13};
        for (int i = 0; i < arr.length - 1; i++) {
            int min = i;
            for (int j = i + 1; j < arr.length; j++)
                if (arr[j] < arr[min])
                    min = j;

            int temp = arr[min];
            arr[min] = arr[i];
            arr[i] = temp;
        }

        for (int num : arr)
            System.out.print(num + " ");
    }
}
""",
   
    "insertion_sort": """
public class InsertionSort {
    public static void main(String[] args) {
        int[] arr = {8, 4, 1, 5, 9};
      
      for(int i = 1; i < arr.length; i++) {
        int key = arr[i];
        int j = i - 1;
        
        while(j >= 0 && arr[j] > key) {
          arr[j + 1] = arr[j];
          j--;
        }

        arr[j + 1] = key;
      }
      
      for(int num : arr) {
        System.out.print(num + " ");
      }
   }
}
""",

    "merge_sort": """
public class MergeSort {
    public static void mergeSort(int[] arr, int l, int r) {
        if (l < r) {
            int m = (l + r) / 2;
            mergeSort(arr, l, m);
            mergeSort(arr, m + 1, r);
            merge(arr, l, m, r);
        }
    }

    public static void merge(int[] arr, int l, int m, int r) {
        int[] left = java.util.Arrays.copyOfRange(arr, l, m + 1);
        int[] right = java.util.Arrays.copyOfRange(arr, m + 1, r + 1);
        int i = 0, j = 0, k = l;

        while (i < left.length && j < right.length)
            arr[k++] = (left[i] <= right[j]) ? left[i++] : right[j++];

        while (i < left.length) arr[k++] = left[i++];
        while (j < right.length) arr[k++] = right[j++];
    }

    public static void main(String[] args) {
        int[] arr = {38, 27, 43, 3, 9, 82, 10};
        mergeSort(arr, 0, arr.length - 1);
        for (int num : arr)
            System.out.print(num + " ");
    }
}
""",

    "quick_sort": """
public class QuickSort {
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    public static int partition(int[] arr, int low, int high) {
        int pivot = arr[high], i = low - 1;
        for (int j = low; j < high; j++)
            if (arr[j] < pivot)
                swap(arr, ++i, j);
        swap(arr, i + 1, high);
        return i + 1;
    }

    public static void swap(int[] arr, int i, int j) {
        int t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }

    public static void main(String[] args) {
        int[] arr = {10, 7, 8, 9, 1, 5};
        quickSort(arr, 0, arr.length - 1);
        for (int num : arr)
            System.out.print(num + " ");
    }
}
""",

    "matrix addition": """
public class Main {
    public static void main(String[] args) {
        int[][] a = {{1, 2}, {3, 4}};
        int[][] b = {{5, 6}, {7, 8}};
        int[][] sum = new int[2][2];
        for (int i = 0; i < 2; i++)
            for (int j = 0; j < 2; j++)
                sum[i][j] = a[i][j] + b[i][j];
        for (int[] row : sum) {
            for (int n : row)
                System.out.print(n + " ");
            System.out.println();
        }
    }
}
""",

    "matrix multiplication": """
public class Main {
    public static void main(String[] args) {
        int[][] a = {{1, 2}, {3, 4}};
        int[][] b = {{2, 0}, {1, 2}};
        int[][] result = new int[2][2];

        for (int i = 0; i < 2; i++)
            for (int j = 0; j < 2; j++)
                for (int k = 0; k < 2; k++)
                    result[i][j] += a[i][k] * b[k][j];

        for (int[] row : result) {
            for (int n : row)
                System.out.print(n + " ");
            System.out.println();
        }
    }
}
""",

    "try catch example": """
public class Main {
    public static void main(String[] args) {
        try {
            int a = 10 / 0;
        } catch (ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
""",

    "string builder reverse": """
public class Main {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder("Copilot");
        System.out.println(sb.reverse());
    }
}
""",

    "constructor example": """
class Car {
    String model;
    Car(String m) {
        model = m;
    }
    void display() {
        System.out.println("Model: " + model);
    }

    public static void main(String[] args) {
        Car c = new Car("BMW");
        c.display();
    }
}
""",

    "inheritance example": """
class Animal {
    void sound() {
        System.out.println("Animal makes sound");
    }
}
class Dog extends Animal {
    void sound() {
        System.out.println("Dog barks");
    }

    public static void main(String[] args) {
        Animal a = new Dog();
        a.sound();
    }
}
""",

    "file write": """
import java.io.FileWriter;
public class Main {
    public static void main(String[] args) {
        try {
            FileWriter fw = new FileWriter("output.txt");
            fw.write("Hello, file!");
            fw.close();
            System.out.println("Written to file.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
""",

    "factorial_using_recursion": """
public class Main {
    static int factorial(int n) {
        if (n == 0) return 1;
        return n * factorial(n - 1);
    }
    public static void main(String[] args) {
        System.out.println("Factorial: " + factorial(5));
    }
}
""",

    "fibonacci_nth term using_recursion": """
public class Main {
    static int fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }
    public static void main(String[] args) {
        System.out.println("Fibonacci(6): " + fib(6));
    }
}
""",

    "reverse_a string using_recursion": """
public class Main {
    static String reverse(String str) {
        if (str.isEmpty()) return str;
        return reverse(str.substring(1)) + str.charAt(0);
    }
    public static void main(String[] args) {
        System.out.println("Reversed: " + reverse("hello"));
    }
}
""",

    "check_palindrome string using_recursion": """
public class Main {
    static boolean isPalindrome(String s, int l, int r) {
        if (l >= r) return true;
        if (s.charAt(l) != s.charAt(r)) return false;
        return isPalindrome(s, l + 1, r - 1);
    }
    public static void main(String[] args) {
        String str = "madam";
        System.out.println(isPalindrome(str, 0, str.length() - 1) ? "Palindrome" : "Not Palindrome");
    }
}
""",

    "print_1 to n using_recursion": """
public class Main {
    static void print1toN(int n) {
        if (n == 0) return;
        print1toN(n - 1);
        System.out.print(n + " ");
    }
    public static void main(String[] args) {
        print1toN(5);
    }
}
""",

    "print_n to 1 using_recursion": """
public class Main {
    static void printNto1(int n) {
        if (n == 0) return;
        System.out.print(n + " ");
        printNto1(n - 1);
    }
    public static void main(String[] args) {
        printNto1(5);
    }
}
""",

    "sum_of first n natural numbers using_recursion": """
public class Main {
    static int sum(int n) {
        if (n == 0) return 0;
        return n + sum(n - 1);
    }
    public static void main(String[] args) {
        System.out.println("Sum: " + sum(10));
    }
}
""",

    "count_digits using_recursion": """
public class Main {
    static int countDigits(int n) {
        if (n == 0) return 0;
        return 1 + countDigits(n / 10);
    }
    public static void main(String[] args) {
        System.out.println("Digits: " + countDigits(12345));
    }
}
""",

    "reverse_number using_recursion": """
public class Main {
    static int reverse(int n, int rev) {
        if (n == 0) return rev;
        return reverse(n / 10, rev * 10 + n % 10);
    }
    public static void main(String[] args) {
        System.out.println("Reversed: " + reverse(1234, 0));
    }
}
""",

    "reverse_array using_recursion": """
import java.util.Scanner;

public class Main {

    static void printReverse(int[] array, int index) {
        if (index < 0) return; // Base case: stop when index is out of bounds
        System.out.print(array[index] + " ");
        printReverse(array, index - 1); // Recursive call to the previous element
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int size = scanner.nextInt(); // Read number of elements
        int[] numbers = new int[size];

        for (int i = 0; i < size; i++) {
            numbers[i] = scanner.nextInt(); // Store input in array
        }

        printReverse(numbers, size - 1); // Start printing from the last element
    }
}
""",

    "reverse_array without_recursion": """
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int size = scanner.nextInt(); // Read number of elements
        int[] numbers = new int[size];

        for (int i = 0; i < size; i++) {
            numbers[i] = scanner.nextInt(); // Fill the array
        }

        // Print array in reverse using a loop
        for (int i = size - 1; i >= 0; i--) {
            System.out.print(numbers[i] + " ");
        }
    }
}
""",

    "check_array sorted using_recursion": """
public class Main {
    static boolean isSorted(int[] arr, int i) {
        if (i == arr.length - 1) return true;
        if (arr[i] > arr[i + 1]) return false;
        return isSorted(arr, i + 1);
    }
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        System.out.println(isSorted(arr, 0) ? "Sorted" : "Not Sorted");
    }
}
""",

    "find_max in array using_recursion": """
public class Main {
    static int findMax(int[] arr, int i) {
        if (i == arr.length - 1) return arr[i];
        return Math.max(arr[i], findMax(arr, i + 1));
    }
    public static void main(String[] args) {
        int[] arr = {3, 9, 2, 7, 5};
        System.out.println("Max: " + findMax(arr, 0));
    }
}
""",

    "sum_of_odd_and_even_numbers_expanded": """
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int count = sc.nextInt(); // Read how many numbers user wants to input

        int[] numbers = new int[count];
        for (int i = 0; i < count; i++) {
            numbers[i] = sc.nextInt(); // Fill array with input values
        }

        int sumOfOdd = 0;
        int sumOfEven = 0;

        for (int i = 0; i < count; i++) {
            if (numbers[i] % 2 == 0) {
                // Expanded form: sumOfEven = sumOfEven + numbers[i];
                sumOfEven = sumOfEven + numbers[i];
            } else {
                // Expanded form: sumOfOdd = sumOfOdd + numbers[i];
                sumOfOdd = sumOfOdd + numbers[i];
            }
        }
        System.out.println(sumOfOdd + " " + sumOfEven); // Print: odd sum first, then even sum
    }
}
""",

    "count_positive_negative_zero": """
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int arraySize = sc.nextInt(); // Read how many numbers will be entered

        int zeroCount = 0;
        int positiveCount = 0;
        int negativeCount = 0;

        for (int idx = 0; idx < arraySize; idx++) {
            int num = sc.nextInt(); // Read the current number

            if (num == 0) {
                zeroCount = zeroCount + 1; // Increase zero counter
            } else if (num > 0) {
                positiveCount = positiveCount + 1; // Increase positive counter
            } else {
                negativeCount = negativeCount + 1; // Increase negative counter
            }
        }

        // Print the final counts
        System.out.println(zeroCount + " " + positiveCount + " " + negativeCount);
    }
}
""",

    "sum_of array elements using_recursion": """
public class Main {
    static int sumArray(int[] arr, int i) {
        if (i == arr.length) return 0;
        return arr[i] + sumArray(arr, i + 1);
    }
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        System.out.println("Sum: " + sumArray(arr, 0));
    }
}
""",

    "smartInterviews_Max Element in Array": """
import java.io.*;
import java.util.*;

public class Main {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Main. */
        Scanner sc = new Scanner(System.in);

        int num = sc.nextInt();
        int[] arr = new int[num];

        for(int m = 0; m < num; m++)
        {
            arr[m] = sc.nextInt();
        }
        int ans = arr[0];

        for(int e = 0; e<num; e++)
        {
            ans = Math.max(ans, arr[e]);
        } 

        System.out.println(ans);
    }
}
""",

    "smartInterviews_Number Distribution": """

import java.io.*;
import java.util.*;

public class Main {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Main. */
        Scanner sc = new Scanner(System.in);

        int arraySize = sc.nextInt();

        int ZeroCount = 0;
        int PositiveCount = 0;
        int NegativeCount = 0;

        for(int idx = 0; idx<arraySize; idx++)
        {
            int num = sc.nextInt();

            if(num == 0){
                ZeroCount++;
            } else if (num > 0) {
                PositiveCount++;
            } else {
                NegativeCount++;
            }
        }
        System.out.println(ZeroCount+ " " +PositiveCount+ " " +NegativeCount);
    }
}
""",

    "smartInterviews_Reverse Array": """
import java.io.*;
import java.util.*;

public class Main {

    public static void printReverse(int[] arr, int index)     //printReverse function to reverse the array
    {
        if(index < 0) 
        {
            return;
        }
        System.out.print(arr[index]+" ");
        printReverse(arr, index-1);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int nums = sc.nextInt();
        int[] arr = new int [nums];

        for(int r = 0; r<nums; r++)
        {
            arr[r] = sc.nextInt();
        }
        printReverse(arr, nums-1);
    }
}
""",

    "smartInterviews_Odd and Even Sum": """
import java.io.*;
import java.util.*;

public class Main {

    public static void main(String[] args) {
        
        Scanner sc = new Scanner(System.in);

        int num = sc.nextInt();
        int[] arr = new int[num];

        for(int s=0; s < num; s++) 
        {
            arr[s] = sc.nextInt();
        }

        int sumOfOdd = 0, sumOfEven = 0;

        for(int i = 0; i < num; i++)
        {
            if(arr[i]%2 == 0) {

                sumOfEven += arr[i];
            } else {
                sumOfOdd += arr[i];

            }
        }
        System.out.println(sumOfOdd +" "+ sumOfEven);        //Print the result for Odd and Even Sum
    }
}
""",

    "smartInterviews_Find Duplicate Num in Array": """
import java.io.*;
import java.util.*;

public class Main {

    public static void main(String[] args) {
        
        Scanner sc = new Scanner(System.in);
        int sizeOfArray = sc.nextInt();

        long[] data = new long[sizeOfArray];

        for(int i = 0; i<sizeOfArray; i++)
        {
            data[i] = sc.nextLong();
        }

        for(int p=0; p < sizeOfArray; p++) {

            for(int q = p + 1; q<sizeOfArray; q++) {

                if(data[p] == data[q]) {
                    System.out.println(data[p]);
                    return;
                }
            }
        }
    }
}
""",
 
    "smartInterviews_Merge Two Sorted Arrays": """
import java.io.*;
import java.util.*;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int sizeoFA = sc.nextInt();
        int[] arrA = new int[sizeoFA];

        for(int i = 0; i < sizeoFA; i++)
        {
            arrA[i] = sc.nextInt();
        }

        int sizeoFB = sc.nextInt();
        int[] arrB = new int[sizeoFB];

        for(int j=0; j < sizeoFB; j++) 
        {
            arrB[j] = sc.nextInt();
        }

        int indexOfA = 0;
        int indexOfB = 0;

        while(indexOfA < sizeoFA && indexOfB < sizeoFB)
        {
            if(arrA[indexOfA]<=arrB[indexOfB]) {

                System.out.print(arrA[indexOfA]+" ");
                indexOfA++;
            } else {
                System.out.print(arrB[indexOfB] + " ");
                indexOfB++;

            }
        }
        while (indexOfA < sizeoFA) {
            System.out.print(arrA[indexOfA] +" ");
            indexOfA++;
        }

        while(indexOfB<sizeoFB)
        {
            System.out.print(arrB[indexOfB]+ " ");
            indexOfB++;
        }
    }
}
""",

    "smartInterviews_The Missing Number": """
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int totalNum = 100;
        int ExpectedSUM = totalNum * (totalNum+1) / 2;
        int CurrentSum =  0;

        for(int n=0; n < totalNum - 1 ; n++)
        {
            CurrentSum += sc.nextInt();
        }
        int MissingNum = ExpectedSUM - CurrentSum;
        System.out.println(MissingNum);
    }
}
""",

    "smartInterview_Prime or not": """
import java.util.Scanner;

public class SimplePrimeCheck {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a number: ");
        int num = sc.nextInt();

        int count = 0;
        for (int i = 1; i <= num; i++) {
            if (num % i == 0) {
                count++;
            }
        }

        if (count == 2) {
            System.out.println(num + " is a Prime number.");
        } else {
            System.out.println(num + " is Not a Prime number.");
        }

        sc.close();
    }
}
""",

    "file read": """
import java.io.FileReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        try {
            FileReader fr = new FileReader("output.txt");
            int ch;
            while ((ch = fr.read()) != -1)
                System.out.print((char) ch);
            fr.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
"""
}
from .pattern_codes_in_java import java_pattern_answers
java_answers.update(java_pattern_answers)

from .array_codes_in_java import java_array_answers
java_answers.update(java_array_answers)

# === Java Question Handler ===

async def handle_java_question(update, context):
    text = update.message.text.strip().lower()

    if not text.startswith("/java "):
        return False

    query = text[6:].strip()

    # Normalize dictionary for case-insensitive lookup
    normalized_answers = {k.lower(): v for k, v in java_answers.items()}
    found_key = normalized_answers.get(query)

    if found_key:
        print(f"[JAVA DEBUG] Match found: {found_key.title()}")
        answer = normalized_answers[found_key].strip()
        # Safely format
        formatted = f"```java\n{answer}\n```"
        try:
            await update.message.reply_text(formatted, parse_mode="Markdown")
        except Exception as e:
            print(f"[JAVA DEBUG] Markdown error: {e}")
            await update.message.reply_text(answer)  # fallback plain text
    else:
        print("[JAVA DEBUG] No match found.")
        await update.message.reply_text("❌ Sorry, I don't have that Java program yet.")

    return True

# === Utility: Get all available topics ===
def get_available_java_topics():
    return sorted(java_answers.keys())