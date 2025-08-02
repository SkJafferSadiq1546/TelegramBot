
java_pattern_answers = {
    
    "pattern_number_triangle": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++)
                System.out.print(j + " ");
            System.out.println();
        }
    }
}
""",

    "pattern_reverse_number_triangle": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = n; i >= 1; i--) {
            for (int j = 1; j <= i; j++)
                System.out.print(j + " ");
            System.out.println();
        }
    }
}
""",

    "pattern_same_number_triangle": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++)
                System.out.print(i + " ");
            System.out.println();
        }
    }
}
""",

    "pattern_right_angled_triangle": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++)
                System.out.print("* ");
            System.out.println();
        }
    }
}
""",

    "pattern_inverted_triangle": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = n; i >= 1; i--) {
            for (int j = 1; j <= i; j++)
                System.out.print("* ");
            System.out.println();
        }
    }
}
""",

    "alphabet triangle pattern": """
public class Main {
    public static void main(String[] args) {
        char ch = 'A';
        for (int i = 1; i <= 5; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(ch + " ");
                ch++;
            }
            System.out.println();
        }
    }
}
""",

    "pattern_pyramid": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int s = 1; s <= n - i; s++)
                System.out.print(" ");
            for (int j = 1; j <= (2 * i - 1); j++)
                System.out.print("*");
            System.out.println();
        }
    }
}
""",

    "pattern_inverted_pyramid": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = n; i >= 1; i--) {
            for (int s = 1; s <= n - i; s++)
                System.out.print(" ");
            for (int j = 1; j <= (2 * i - 1); j++)
                System.out.print("*");
            System.out.println();
        }
    }
}
""",

    "pattern_hollow_pyramid": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int s = 1; s <= n - i; s++)
                System.out.print(" ");
            for (int j = 1; j <= (2 * i - 1); j++) {
                if (j == 1 || j == (2 * i - 1) || i == n)
                    System.out.print("*");
                else
                    System.out.print(" ");
            }
            System.out.println();
        }
    }
}
""",

    "pattern_number_pyramid": """
public class Main {
    public static void main(String[] args) {
        int n = 5, num = 1;
        for (int i = 1; i <= n; i++) {
            for (int s = 1; s <= n - i; s++)
                System.out.print(" ");
            for (int j = 1; j <= i; j++)
                System.out.print(num++ + " ");
            System.out.println();
        }
    }
}
""",

    "pattern_hollow_inverted_pyramid": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = n; i >= 1; i--) {
            for (int s = 1; s <= n - i; s++)
                System.out.print(" ");
            for (int j = 1; j <= 2 * i - 1; j++) {
                if (i == n || j == 1 || j == 2 * i - 1)
                    System.out.print("*");
                else
                    System.out.print(" ");
            }
            System.out.println();
        }
    }
}
""",

    "pattern_diamond": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        // upper half
        for (int i = 1; i <= n; i++) {
            for (int s = 1; s <= n - i; s++)
                System.out.print(" ");
            for (int j = 1; j <= (2 * i - 1); j++)
                System.out.print("*");
            System.out.println();
        }
        // lower half
        for (int i = n - 1; i >= 1; i--) {
            for (int s = 1; s <= n - i; s++)
                System.out.print(" ");
            for (int j = 1; j <= (2 * i - 1); j++)
                System.out.print("*");
            System.out.println();
        }
    }
}
""",


    "pattern_alphabet_diamond": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int s = 1; s <= n - i; s++)
                System.out.print(" ");
            for (char ch = 'A'; ch < 'A' + i; ch++)
                System.out.print(ch);
            for (char ch = (char) ('A' + i - 2); ch >= 'A'; ch--)
                System.out.print(ch);
            System.out.println();
        }
    }
}
""",

    "pattern_alphabet_triangle": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        char ch = 'A';
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++)
                System.out.print(ch + " ");
            ch++;
            System.out.println();
        }
    }
}
""",

    "pattern_right_alphabet_triangle": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (char i = 'A'; i <= 'A' + n - 1; i++) {
            for (char j = 'A'; j <= i; j++)
                System.out.print(j + " ");
            System.out.println();
        }
    }
}
""",

    "pattern_reverse_alphabet_triangle": """
public class Main {
    public static void main(String[] args) {
        char ch = 'E';
        for (int i = 5; i >= 1; i--) {
            for (int j = 1; j <= i; j++)
                System.out.print(ch + " ");
            ch--;
            System.out.println();
        }
    }
}
""",

    "pattern_alphabet_pyramid": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 0; i < n; i++) {
            char ch = 'A';
            for (int s = 1; s <= n - i - 1; s++)
                System.out.print(" ");
            for (int j = 0; j <= i; j++)
                System.out.print(ch++ + " ");
            System.out.println();
        }
    }
}
""",

    "pattern_palindrome_number_triangle": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int s = 1; s <= n - i; s++)
                System.out.print(" ");
            for (int j = i; j >= 1; j--)
                System.out.print(j);
            for (int j = 2; j <= i; j++)
                System.out.print(j);
            System.out.println();
        }
    }
}
""",

    "pattern_alphabet_hill_pattern": """
public class Main {
    public static void main(String[] args) {
        int n = 4;
        for (int i = 0; i < n; i++) {
            for (int s = 1; s <= n - i - 1; s++)
                System.out.print(" ");
            char ch = 'A';
            for (int j = 0; j <= i; j++)
                System.out.print(ch++);
            ch--;
            for (int j = 1; j <= i; j++)
                System.out.print(--ch);
            System.out.println();
        }
    }
}
""",

    "pattern_pascal_triangle": """
public class Main {
    public static void main(String[] args) {
        int rows = 5;
        for (int i = 0; i < rows; i++) {
            int number = 1;
            for (int s = 0; s < rows - i; s++)
                System.out.print(" ");
            for (int j = 0; j <= i; j++) {
                System.out.print(number + " ");
                number = number * (i - j) / (j + 1);
            }
            System.out.println();
        }
    }
}
""",

    "pattern_right_pascal_triangle": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        // upper half
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++)
                System.out.print("* ");
            System.out.println();
        }
        // lower half
        for (int i = n - 1; i >= 1; i--) {
            for (int j = 1; j <= i; j++)
                System.out.print("* ");
            System.out.println();
        }
    }
}
""",

    "pattern_floyds_triangle": """
public class Main {
    public static void main(String[] args) {
        int n = 5, num = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(num + " ");
                num++;
            }
            System.out.println();
        }
    }
}
""",

    "pattern_k_shape": """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 0; i < n; i++) {
            System.out.print("*");
            for (int j = 0; j < n - i - 1; j++)
                System.out.print(" ");
            System.out.print("*");
            System.out.println();
        }
        for (int i = 1; i < n; i++) {
            System.out.print("*");
            for (int j = 0; j < i; j++)
                System.out.print(" ");
            System.out.print("*");
            System.out.println();
        }
    }
}
""",

    "pattern_hollow_rectangle": """
public class Main {
    public static void main(String[] args) {
        int rows = 5, cols = 10;
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= cols; j++) {
                if (i == 1 || i == rows || j == 1 || j == cols)
                    System.out.print("*");
                else
                    System.out.print(" ");
            }
            System.out.println();
        }
    }
}
""",

    "pattern_star_pyramid": """
public class Main {
    public static void main(String[] args) {
        int rows = 5;
        for (int i = 1; i <= rows; i++) {
            for (int j = i; j < rows; j++)
                System.out.print(" ");
            for (int k = 1; k <= (2 * i - 1); k++)
                System.out.print("*");
            System.out.println();
        }
    }
}

Output  -> 👇   

    *
   ***
  *****
 *******
*********
"""
}