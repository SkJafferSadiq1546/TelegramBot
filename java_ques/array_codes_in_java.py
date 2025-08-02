java_array_answers = {
    
    "Find the Largest Element in an Array":"""
    import java.util.Scanner;

public class MaxInArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];

        for(int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int max = arr[0];
        for(int i = 1; i < n; i++) {
            if(arr[i] > max)
                max = arr[i];
        }   

        System.out.println("Largest element: " + max);
    }
}
""",

    "Find the Smallest Element in an Array":"""
    import java.util.Scanner;

public class MinInArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];

        for(int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int min = arr[0];
        for(int i = 1; i < n; i++) {
            if(arr[i] < min)
                min = arr[i];
        }

        System.out.println("Smallest element: " + min);
    }
}
""",

    "Sum of All Elements in an Array":"""
    import java.util.Scanner;

public class SumArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), sum = 0;
        int[] arr = new int[n];

        for(int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
            sum += arr[i];
        }

        System.out.println("Sum: " + sum);
    }
}
""",

    "Reverse the Array":"""
    import java.util.Scanner;

public class ReverseArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];

        for(int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        System.out.print("Reversed: ");
        for(int i = n - 1; i >= 0; i--) {
            System.out.print(arr[i] + " ");
        }
    }
}
""",

    "Count Even and Odd Numbers in an Array":"""
    import java.util.Scanner;

public class EvenOddCount {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), even = 0, odd = 0;
        int[] arr = new int[n];

        for(int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
            if(arr[i] % 2 == 0) even++;
            else odd++;
        }

        System.out.println("Even: " + even);
        System.out.println("Odd: " + odd);
    }
}
""",

    "Find Second Largest Element In an Array":"""
    import java.util.Scanner;

public class SecondLargest {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];

        for(int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int first = Integer.MIN_VALUE, second = Integer.MIN_VALUE;

        for(int num : arr) {
            if(num > first) {
                second = first;
                first = num;
            } else if(num > second && num != first) {
                second = num;
            }
        }

        System.out.println("Second largest: " + second);
    }
}
""",

    "Merge Two Arrays":"""
    import java.util.Scanner;

public class MergeArrays {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n1 = sc.nextInt();
        int[] a = new int[n1];
        for(int i = 0; i < n1; i++) a[i] = sc.nextInt();

        int n2 = sc.nextInt();
        int[] b = new int[n2];
        for(int i = 0; i < n2; i++) {
            b[i] = sc.nextInt();
        }
        
        int[] merged = new int[n1 + n2];

        for(int i = 0; i < n1; i++) {
            merged[i] = a[i];
        }
        
        for(int i = 0; i < n2; i++) {
            merged[n1 + i] = b[i];
        }

        System.out.print("Merged: ");
        for(int x : merged) {
            System.out.print(x + " ");
        }
    }
}
"""
}